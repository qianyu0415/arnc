import shutil
from arnc import app, db, jwt
from arnc.models import Account, Video, Bg, Mask
from flask import  make_response, render_template_string, request, send_file, jsonify, send_from_directory, session
from flask import url_for 
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
from zoneinfo import ZoneInfo


# 导入python常规
import os
import sys
import subprocess
import torch
import gc
from werkzeug.utils import secure_filename
import tempfile
import numpy as np
from pathlib import Path

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound


# 导入impainting anything
sys.path.append('./models/ia')
from image_processor import process_image_rembg, process_image

sys.path.append('./models/combine-anything')
from convert import convert_glb_to_gltf


# 定义一些和路径有关的全局变量
repo_dir = "/root/autodl-tmp/arnc_project/arnc/static/repo"




# 路由定义区
@app.errorhandler(RuntimeError)
def handle_cuda_out_of_memory_error(error):

    error_str = str(error)

    # 全局处理cuda内存不足的问题
    if "CUDA out of memory" in error_str:

        print("CUDA 内存不足，正在尝试释放内存...")
        gc.collect()
        torch.cuda.empty_cache()
        # 返回一个错误响应或者重定向到一个错误页面
        return "CUDA 内存不足，已尝试释放内存。请重试操作。", 500
    # 如果不是 CUDA 内存不足的错误，继续抛出异常

    return error_str, 500


# 注册路由
@app.route('/user/register', methods = ['POST'])
def register():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    account = Account(name=name, email=email, password=password)

    db.session.add(account)


    try:
        db.session.commit()

        account_dir = os.path.join(repo_dir, email)

        if not os.path.exists(account_dir):
            os.makedirs(account_dir)
            print(f"Directory '{account_dir}' was created.")
        else:
            print(f"Directory '{account_dir}' already exists.")


        # 依据注册信息为用户创建仓库
        video3D_dir = os.path.join(account_dir, "video3D")
        videoAA_dir = os.path.join(account_dir, "videoAA")
        bg_dir = os.path.join(account_dir, 'bg')
        mask_dir = os.path.join(account_dir, 'mask')
        cache_dir = os.path.join(account_dir, 'cache')

        os.mkdir(video3D_dir)
        os.mkdir(videoAA_dir)
        os.mkdir(bg_dir)
        os.mkdir(mask_dir)
        os.mkdir(cache_dir)
        
        return jsonify({"message": "账户创建成功"}), 200
    
    except IntegrityError as e:
        
        db.session.rollback()  # 回滚会话以保持数据一致性
        error_info = str(e.orig)  # 获取原始错误信息
        
        if 'name' in error_info:
            error_message = f'名称 "{name}" 已经被使用。'
            
        elif 'email' in error_info:
            error_message = f'邮件 "{email}" 已经被注册。'
            
        else:
            error_message = '发生了未知的数据库错误。'
            
        return jsonify({"error": error_message}), 400
    

# 登录界面
@app.route('/user/login', methods=['POST'])
def login():
    
    # 从前端的form表单获取邮件和密码信息
    email = request.form['email']
    password = request.form['password']

    try:
        # 使用邮箱对数据库信息进行检索
        acc = Account.query.filter(Account.email == email).one()
        
        if acc.password == password:
            # 以邮箱作为令牌
            access_token = create_access_token(identity = email)
            # 登录成功
            return jsonify({"message": "登录成功", "access_token":access_token}), 200
        else:
            # 密码错误
            return jsonify({"message": "密码错误"}), 401
    except NoResultFound:
        # 用户不存在
        return jsonify({"message": "用户不存在"}), 401


# 自动补全人物空隙
@app.route('/inpainting_automatically', methods=['POST'])
@jwt_required()
def handle_image_processing():
    
    # 检查是否有文件在请求中
    if 'input_img' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['input_img']

    acc_email = get_jwt_identity()
    
    # 如果用户没有选择文件，浏览器也会提交一个空的文件部分
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    
    # 获取北京时间（UTC+8）
    time = datetime.now(ZoneInfo("Asia/Shanghai"))

    # 格式化时间字符串，例如：2023-03-10_12-30-00
    formatted_time = time.strftime("%Y-%m-%d_%H-%M-%S")

    # 构建文件名
    file_extension = os.path.splitext(file.filename)[1]
    filename = "image_" + formatted_time + file_extension

    # 保存上传的文件到临时目录
    input_img_path = os.path.join(repo_dir, acc_email,"cache", filename)
    file.save(input_img_path)

    # 从form表单中获取部分信息
    dilate_kernel_size = request.form.get('dilate_kernel_size', type=int)
    sam_model_type = request.form.get('sam_model_type', default='vit_h')
    sam_ckpt = request.form.get('sam_ckpt','./models/ia/pretrained_models/sam_vit_h_4b8939.pth')
    lama_config = request.form.get('lama_config', default='./models/ia/lama/configs/prediction/default.yaml')
    lama_ckpt = request.form.get('lama_ckpt','./models/ia/pretrained_models/big-lama')
    
    # 构建用户仓库的路径
    output_dir = os.path.join(repo_dir, acc_email )  

    # 假设 process_image 函数返回处理后图像的路径
    output_img_path = process_image_rembg(input_img=input_img_path, 
                                    dilate_kernel_size=dilate_kernel_size, 
                                    output_dir=output_dir,
                                    sam_model_type=sam_model_type, 
                                    sam_ckpt=sam_ckpt, 
                                    lama_config=lama_config, 
                                    lama_ckpt=lama_ckpt)
    
    # 将上传的图片删除
    os.remove(input_img_path)

    # 构建生成的背景图像和掩模的对应地址
    M1_dir = os.path.join(output_dir, 'mask', filename)
    bg1_dir = os.path.join(output_dir, 'bg', filename)

    # 检索账号
    acc_id = Account.query.filter(Account.email == acc_email).one()

    # 将背景图片的信息增加入数据库
    Bg1 = Bg(name = filename, dir = bg1_dir, account_id = acc_id.id)
    db.session.add(Bg1)
    db.session.commit()
    
    # 检索bg_id, 用作Mask的外键
    bg_id = Bg.query.filter(Bg.dir == bg1_dir).one( )
    M1 = Mask(name = filename, dir = M1_dir, account_id = acc_id.id, bg_id = bg_id.id )
    db.session.add(M1)

    db.session.commit()

    # 返回处理后的图像
    return send_file(output_img_path, mimetype='image/png')


# 选点补全人物空隙
@app.route('/inpainting', methods=['POST'])
@jwt_required()
def handle_process_image():
    if request.method == 'POST':
        
        # 检查是否有文件在请求中
        if 'image' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files.get('image',None)

        # 检验防止用户上传一个空文件
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        acc_email = get_jwt_identity()

        # 获取北京时间（UTC+8）
        time = datetime.now(ZoneInfo("Asia/Shanghai"))

        # 格式化时间字符串，例如：2023-03-10_12-30-00
        formatted_time = time.strftime("%Y-%m-%d_%H-%M-%S")

        # 假设你要保存的是一个图片文件，可以这样构建文件名
        file_extension = os.path.splitext(file.filename)[1]
        filename = "image_" + formatted_time + file_extension

        # 保存上传的文件到临时目录
        input_img_path = os.path.join(repo_dir, acc_email,"cache", filename)
        file.save(input_img_path)
        
        # 设置一部分表单信息
        point_coords = request.form.get('point_coords')
        point_labels = request.form.get('point_labels','1')

        sam_model_type = request.form.get('sam_model_type','vit_h')

        sam_ckpt_path = request.form.get('sam_ckpt_path','./models/ia/pretrained_models/sam_vit_h_4b8939.pth')
        lama_config_path = request.form.get('lama_config_path','./models/ia/lama/configs/prediction/default.yaml')
        lama_ckpt_path = request.form.get('lama_ckpt_path','./models/ia/pretrained_models/big-lama')

        # 构建用户的仓库路径
        save_dir = os.path.join(repo_dir, acc_email)
        # 对图像进行处理
        output_path = process_image(input_img_path, point_coords, point_labels, sam_model_type, sam_ckpt_path, lama_config_path, lama_ckpt_path, save_dir, filename)
        
        # 移除上传的图片
        os.remove(input_img_path)
        
        # 构建图像和掩模的文件路径
        M1_dir = os.path.join(save_dir, 'mask', filename)
        bg1_dir = os.path.join(save_dir, 'bg', filename)

        # 数据库检索查询账号
        acc_id = Account.query.filter(Account.email == acc_email).one()

        # 将背景图片和掩模的相关信息添加进入数据库
        Bg1 = Bg(name = filename, dir = bg1_dir, account_id = acc_id.id)
        db.session.add(Bg1)
        db.session.commit()
        
        bg_id = Bg.query.filter(Bg.dir == bg1_dir).one( )
        M1 = Mask(name = filename, dir = M1_dir, account_id = acc_id.id, bg_id = bg_id.id )
         
        db.session.add(M1)

        db.session.commit()
        
        try:
            return send_file(output_path, mimetype='image/png')
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        
              
# magicAnimate自动生成动画（目前是脚本嵌套模式，后续可以考虑再换回函数的形式
@app.route('/magic-animate', methods = ['POST'])
@jwt_required()
def image_to_video():
    if request.method == 'POST':
        
        judge = 0   # 用于判断用户选择图片的方式，如果用户选择了一张图片库中的图，则不变
        acc_email = get_jwt_identity()
        
        if 'imageFile' not in request.files:
            path_img = request.form['path_img']
            
        else:
            file = request.files.get('imageFile',None)

            if file.filename == '':
                return jsonify({'error': 'No selected file'}), 400
        
            # 获取北京时间（UTC+8）
            time = datetime.now(ZoneInfo("Asia/Shanghai"))

            # 格式化时间字符串，例如：2023-03-10_12-30-00
            formatted_time = time.strftime("%Y-%m-%d_%H-%M-%S")

            # 构建文件名
            file_extension = os.path.splitext(file.filename)[1]
            filename = "image_" + formatted_time + file_extension

            # 保存上传的文件到临时目录
            path_img = os.path.join(repo_dir, acc_email,"cache", filename)
            file.save(path_img)
            judge = 1       # 用户选择了上传一张图片，则judge置为1
        
        # 获取前端发送的视频文件路径
        path_vid = request.form['path_vid']

        # 指定输出视频路径
        output_dir = os.path.join(repo_dir, acc_email, 'videoAA')
        
        # 调用先前的Python脚本进行处理
        try:
            subprocess.run([
                "python3", "./models/ma/magicanimate/pipelines/animation.py",
                "--config", "./models/ma/configs/prompts/animation.yaml",
                "--image_path", path_img,
                "--video_path", path_vid,
                "--save_dir", output_dir,  
                "--dist"
            ], check=True)
            
        except subprocess.CalledProcessError as e:
            # 处理发生错误
            return jsonify({"error": str(e)}), 500  
            
        # 若用户上传了一张照片，则把它删除
        if judge == 1:
            os.remove(path_img)
            
        # 构建保存文件路径
        filename = Path(path_vid).stem + '_' + Path(path_img).stem + '.mp4'
        output_file = os.path.join(output_dir, filename )
        
        
        # 获取北京时间（UTC+8）
        time = datetime.now(ZoneInfo("Asia/Shanghai"))

        # 格式化时间字符串，例如：2023-03-10_12-30-00
        formatted_time = time.strftime("%Y-%m-%d_%H-%M-%S")

        # 构建文件名
        file_extension = '.mp4'
        filename = "video_" + formatted_time + file_extension
        
        # 对MagicAnimate生成的文件进行重命名，便于视频存储系统的管理
        Path(output_file).rename(Path(output_file).parent / filename)
        path_parts = output_file.split(os.sep)

        # 修改文件名称
        path_parts[-1] = filename

        # 重新组合路径
        output_file = os.sep.join(path_parts)
            
        # 将生成视频信息添加到数据库中
        acc_id = Account.query.filter(Account.email == acc_email).one()
        V1 = Video(type = 'ma', name = filename, dir = output_file, account_id = acc_id.id)
        
        db.session.add(V1)
        db.session.commit()
            
        print(output_file)

        # 如果视频文件生成成功，发送给前端
        return send_file(output_file, mimetype='video/mp4')
        
        
        
@app.route('/select-bg', methods = ['POST', 'GET'])
@jwt_required()
def select_bg():
    if request.method == 'GET':
        
        acc_email = get_jwt_identity()
        # 检索账号曾经生成过的全部背景信息列表
        acc_id = Account.query.filter_by(email=acc_email).first().id  
        bg_list = Bg.query.filter_by(account_id=acc_id).all()
        
        if not bg_list:
            # 如果背景图列表为空，根据应用逻辑处理
            return jsonify([])  #如果用户尚且还没创建背景，先返回一个空列表
        
        image_urls = [{bg.dir : url_for('static', filename=f"repo/{acc_email}/bg/{bg.name}")}for bg in bg_list]

        return jsonify(image_urls)  # 使用 jsonify 来返回 JSON 响应
    
         
@app.route('/en3d', methods = ['POST', 'GET'])
@jwt_required()
def en3d():
    if request.method == 'POST':
        # 从表单获取用户的角色和动作id
        charac_id = request.form['charac_id']
        action_id = request.form['action_id']
        
        acc_email = get_jwt_identity()
        
        # 构建cache路径
        cache_dir = os.path.join(repo_dir, acc_email, 'cache')
        
        # 调用子进程，生成3D模型
        try:
            subprocess.run([
                "python", "./models/en3d/animation.py",
                "--charac_id", charac_id,
                "--pose_id", action_id,
                "--save_dir", cache_dir  
            ], check=True)
            
        except subprocess.CalledProcessError as e:
            # 处理发生错误
            return jsonify({"error": str(e)}), 500
        
        # 生成缓存文件glb模型，并对其进行重新命名
        glb_dir = os.path.join(cache_dir, f"{charac_id}-{action_id}.glb")
        glb_name = "a.glb"
        Path(glb_dir).rename(Path(glb_dir).parent / glb_name)

        return jsonify({'message': 'The glb file has been created'}), 200
    

# 定制摄像机角度    
@app.route('/customize', methods = ['POST', 'GET'])
@jwt_required()
def customize():
    if request.method == 'GET':
        # 将en3d路由下生成的glb文件的静态链接返回给前端，从而在前端展示
        acc_email = get_jwt_identity()
        
        glbname = os.path.join("static", "repo", acc_email, "cache", 'a.glb')
        
        return jsonify(glbname)
        
    if request.method == 'POST':
        
        acc_email = get_jwt_identity()
        
        # 首先构建用户仓库的缓存地址
        cache_dir = os.path.join(repo_dir, acc_email, 'cache') 
        
        # 将glb文件先转换成gltf文件
        glb_addr = os.path.join(cache_dir, 'a.glb')
        gltf_addr = os.path.join(cache_dir, 'a.gltf')
        convert_glb_to_gltf(glb_addr, gltf_addr)
        
        # 从form表单获取时间和摄像机参数等信息
        time = request.form['time']
        frames = 24 * int(time) 
        
        bg_path = request.form['bg_path']
        
        pos_x = request.form['pos_x']
        pos_y = request.form['pos_y']
        pos_z = request.form['pos_z']
        
        rad_x = request.form['rad_x']
        rad_y = request.form['rad_y']
        rad_z = request.form['rad_z']
        
        # 调用子进程，使用blender软件对gltf模型进行渲染
        try:
            subprocess.run([
                "./models/en3d/damo/cv_3d-human-animation/3D-assets/blender-3.1.2-linux-x64/blender",
                '--background',
                '--python',
                './models/combine-anything/render_script.py',  # 你需要在你的脚本中添加对这个参数的支持
                '--',
                gltf_addr,
                str(frames),
                cache_dir,
                pos_x,
                pos_y,
                pos_z,
                rad_x,
                rad_y,
                rad_z

            ], check=True)
            
        except subprocess.CalledProcessError as e:
            # 处理发生错误
            return jsonify({"error": str(e)}), 500
        
        
        # 分割路径
        path_parts = bg_path.split(os.sep)

        # 修改倒数第二个目录为 "mask"
        path_parts[-2] = "mask"

        # 重新组合路径
        mask_path = os.sep.join(path_parts)
        
        # 调用子进程，为渲染好的3D模型图片增加背景
        try:
            subprocess.run([
                "python",
                "./models/combine-anything/add_background_cv.py",
                "--save_dir", cache_dir,
                "--bg_mask_path", mask_path,
                "--bg_path", bg_path,
                "--frames", str(frames)

            ], check=True)
        except subprocess.CalledProcessError as e:
            # 处理发生错误
            return jsonify({"error": str(e)}), 500
        
        output_dir = os.path.join(repo_dir, acc_email, 'video3D')
        
        # 获取北京时间（UTC+8）
        time = datetime.now(ZoneInfo("Asia/Shanghai"))

        # 格式化时间字符串，例如：2023-03-10_12-30-00
        formatted_time = time.strftime("%Y-%m-%d_%H-%M-%S")

        
        filename = "video_" + formatted_time 
        
        # 调用子进程，将blender渲染得到的一系列图像作为帧进而生成视频
        try:
            subprocess.run([
                "python",
                "./models/combine-anything/png2video.py",
                "--save_dir", cache_dir,
                "--output_dir", output_dir,
                "--filename", filename

            ], check=True)
        except subprocess.CalledProcessError as e:
            # 处理发生错误
            return jsonify({"error": str(e)}), 500
        
        # 对缓存文件夹中的文件进行清除操作
        frame_dir = os.path.join(cache_dir, 'frame')
        shutil.rmtree(frame_dir)

        for file in os.listdir(cache_dir):
            file_path = os.path.join(cache_dir, file)
            try:
                os.unlink(file_path)
                print(f"已删除 {file_path}")
            except Exception as e:
                print(f"删除 {file_path} 时出错。原因: {e}")
        
        # 构建文件保存路径
        save_dir = os.path.join(repo_dir, acc_email, "video3D")
        
        try:
            output_video_path = os.path.join(save_dir, filename + '.mp4')
            
            # 将生成的视频信息增加到数据库中
            acc_id = Account.query.filter(Account.email == acc_email).one().id

            V1 = Video(type = '3D', name = filename + '.mp4', dir = output_video_path, account_id = acc_id)

            db.session.add(V1)
            db.session.commit()
            
            print("视频路径是" + output_video_path)
            
            url = os.path.join('static','repo', acc_email, 'video3D', filename + '.mp4')
            
            return jsonify({"videoUrl": url})

        except subprocess.CalledProcessError as e:
            # 处理发生错误
            return jsonify({"error": str(e)}), 500
        

# 用于向用户展示用户创作过的作品        
@app.route('/user', methods = ['GET', 'POST'])
@jwt_required()
def show_list( ):
    if request.method == 'GET':
        # 对账户信息进行检索
        acc_email = get_jwt_identity()
        acc = Account.query.filter(Account.email == acc_email).first( )
        acc_id = acc.id
        acc_name = acc.name
        
        # 检索视频和背景图片的相关信息
        Video3D = Video.query.filter((Video.type == '3D') & (Video.account_id == acc_id)).all()
        VideoMA = Video.query.filter((Video.type == 'ma') & (Video.account_id == acc_id)).all()
        bgs = Bg.query.filter(Bg.account_id == acc_id).all()
        
        acc_dir = os.path.join('repo', acc_email)
        
        print(VideoMA)
        
        # 将查询结果转换为列表字典形式，以便jsonify处理
        video3d_list = [{'id': video.id, 'url': url_for('static', filename = os.path.join(acc_dir, 'video3D', video.name))} for video in Video3D]
        videoMA_list = [{'id': video.id, 'url': url_for('static', filename = os.path.join(acc_dir, 'videoAA', video.name))} for video in VideoMA]
        bgs_list = [{'id': bg.id, 'url': url_for('static', filename = os.path.join(acc_dir, 'bg', bg.name) )} for bg in bgs]
        
        print(videoMA_list)
        
        # 使用jsonify返回JSON格式的响应
        return jsonify({'name': acc_name,'email': acc_email, 'Video3D': video3d_list, 'VideoMA': videoMA_list, 'Backgrounds': bgs_list})


