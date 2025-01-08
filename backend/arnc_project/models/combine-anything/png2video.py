import os
import numpy as np
import argparse
import imageio

def parse_args( ):
    parser = argparse.ArgumentParser()
    parser.add_argument("--save_dir", type=str)
    parser.add_argument("--output_dir", type=str)
    parser.add_argument("--filename", type=str)

    args = parser.parse_args()

    return args

if __name__ == '__main__':

    args = parse_args()

    # 指定图片文件夹和输出视频的路径
    image_folder = os.path.join(args.save_dir, 'frame')
    # image_folder = "./test"
    video_path = os.path.join(args.output_dir, args.filename + '.mp4')

    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg") or img.endswith(".png")]
    images.sort(key=lambda x: int(x.split('.')[0]))  # 根据文件名前的数字排序

    
     # 创建视频写入器
    writer = imageio.get_writer(video_path, fps=24)

    # 遍历图片列表，将每张图片添加到视频中
    for img_name in images:
        img_path = os.path.join(image_folder, img_name)
        image = imageio.imread(img_path)
        writer.append_data(image)
    
    # 完成视频写入
    writer.close()

    
