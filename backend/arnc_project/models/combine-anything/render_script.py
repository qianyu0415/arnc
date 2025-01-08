import bpy
import sys
import os
from math import radians
import math
from mathutils import Vector



# 清除初始场景
bpy.ops.wm.read_factory_settings(use_empty=True)

# # 加载glTF文件
# # file_path = 'action.gltf'
# index= sys.argv.index("--") + 1  # 找到 '--' 参数的索引并加1，得到我们需要的参数的索引
# file_path = sys.argv[index]  # 获取文件路径

# 获取 '--' 后的所有参数
try:
    index = sys.argv.index("--") + 1
    # 获取所有 '--' 之后的参数
    params = sys.argv[index:]
except ValueError:
    # 没有找到 '--'，可能的错误处理
    params = []

if len(params) >= 1:
    file_path = params[0]
    frames = int(params[1])
    save_dir = params[2]
    pos_x = float(params[3])
    pos_y = float(params[4])
    pos_z = float(params[5])
    rad_x = float(params[6])
    rad_y = float(params[7])
    rad_z = float(params[8])
    
else:
    print("Not enough arguments provided.")
    # 处理参数不足的情况...

bpy.ops.import_scene.gltf(filepath=file_path)

square = pos_x*pos_x + pos_y*pos_y + pos_z*pos_z
sqrt = math.sqrt(square)

cos_x = pos_x / square
cos_y = pos_y / square
cos_z = pos_z / square

length = 100

pos_x = pos_x + length * cos_x
pos_y = pos_y + length * cos_y
pos_z = pos_z + length * cos_z

'''
# 设置使用Cycles渲染引擎，如果您使用的是Eevee，请相应调整
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.device = 'GPU'
bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'
bpy.context.preferences.addons["cycles"].preferences.get_devices()
for d in bpy.context.preferences.addons["cycles"].preferences.devices:
    # only use GPU.
    if d["name"] == 'Intel Xeon CPU E5-2630 v4 @ 2.20GHz':
        d["use"] = 0 
    else:
        d["use"] = 1
    print(d["name"], d["use"])
'''

# 设置使用Cycles渲染引擎
bpy.context.scene.render.engine = 'CYCLES'

# 启用渲染时降噪
bpy.context.scene.cycles.use_denoising = True

# 选择降噪器类型（例如，'OPTIX'，'OPENIMAGEDENOISE'，或'NLM'）
bpy.context.scene.cycles.denoiser = 'OPENIMAGEDENOISE'

# 设置渲染设备为GPU
bpy.context.scene.cycles.device = 'GPU'

# 设定计算设备类型为CUDA (或者根据你的GPU，你可能需要设置为'OPENCL'或者'OPTIX')
bpy.context.preferences.addons['cycles'].preferences.compute_device_type = 'CUDA'

# 获取所有可用的设备，包括GPU和CPU
bpy.context.preferences.addons["cycles"].preferences.get_devices()

# 遍历所有设备，仅启用GPU设备
for device in bpy.context.preferences.addons["cycles"].preferences.devices:
    if device.type == 'CUDA':  # 或者根据你的设置改为'OPENCL'或'OPTIX'
        device.use = True  # 启用该设备
        print(f"Enabled device: {device.name}")
    else:
        device.use = False  # 禁用非GPU设备

# 确认设置
print("GPU devices are set for rendering.")



bpy.context.scene.cycles.samples = 256
# 开启透明背景
bpy.context.scene.render.film_transparent = True

# 设置渲染输出的文件格式为PNG，并且使用RGBA模式以包括alpha通道
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.image_settings.color_mode = 'RGBA'

# 设置渲染分辨率
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

# 配置渲染路径
bpy.context.scene.render.filepath = os.path.join(save_dir, 'frame')


# 添加相机
# 注意在Blender中，单位通常是米，但是焦距单位是毫米
# bpy.ops.object.camera_add(location=(-5.5457, -18.041, 7.1896))
bpy.ops.object.camera_add(location=(pos_x, pos_y, pos_z))


# 获取新添加的相机对象
camera = bpy.context.object

# 添加Track To约束
track_to = camera.constraints.new(type='TRACK_TO')

# 设置约束的目标为None，相机将对准世界原点
track_to.target = None

# 指定Track To约束的轴
track_to.up_axis = 'UP_Y'
track_to.track_axis = 'TRACK_NEGATIVE_Z'

# 设置相机对准的位置（原点）
camera.constraints["Track To"].target = bpy.data.objects.new(name="TempEmpty", object_data=None)
bpy.context.scene.collection.objects.link(camera.constraints["Track To"].target)

# 移动临时Empty对象到原点
camera.constraints["Track To"].target.location = (0, 0, 1.20)

# # 设置相机的旋转角度，Blender使用的是弧度，所以需要将角度转换为弧度
# # 使用的是欧拉角，需要将您提供的角度转换为弧度

# camera.rotation_euler = (radians(70.599), radians(0.000005), radians(-19.228))

# camera.rotation_mode = 'XYZ'

# camera.rotation_euler = (radians(rad_x), radians(rad_y), radians(rad_z))



# point_camera_at_origin(camera)
print(camera.location)
print(camera.rotation_euler)

# 设置相机的焦距为110mm
camera.data.lens = 110


# 设置相机作为活动相机
bpy.context.scene.camera = camera

# 现在您可以继续进行渲染，让棱角球不可见

object_name = "Polyhedral Sphere"
obj = bpy.data.objects.get(object_name)

if obj:
    obj.hide_render = True


import bpy

'''
# 添加灯光，默认为点光源
bpy.ops.object.light_add(type='POINT', location=(-7.0719, -5.9808, 0))


# 获取新添加的灯光对象
light1 = bpy.context.object

# 设置灯光的能量（瓦特）
light1.data.energy = 1000

# 设置灯光的光照强度、尺寸和阴影
light1.data.specular_factor = 1.0  # 光照的镜面反射强度
light1.data.shadow_soft_size = 3.88  # 阴影柔和度，单位为米

# 因为没有旋转和缩放的变化，这里我们不需要设置这些参数
'''
# 添加点光源到指定位置
bpy.ops.object.light_add(type='POINT', location=(pos_x, pos_y, pos_z))

# 获取新添加的灯光对象
light2 = bpy.context.object

# 设置灯光的能量（瓦特）
light2.data.energy = 7500

# 设置灯光的镜面反射强度
light2.data.specular_factor = 1.0

# 禁用阴影
light2.data.use_shadow = False  # 正确的方式是设置光源数据的use_shadow属性

# # 设置旋转参数
# light2.rotation_euler = (radians(38.624), radians(-37.913), radians(77.554))

start_frame = 1
end_frame = frames

# 遍历动画的每一帧
for frame in range(start_frame, end_frame + 1):
    bpy.context.scene.frame_set(frame)
    frame_path = os.path.join(save_dir, f'frame/{frame}.png')
    bpy.context.scene.render.filepath = frame_path
    bpy.ops.render.render(write_still=True)
