import subprocess

# Blender的安装路径（根据您的系统环境调整）
blender_executable_path = '/home/ac/envpkgs/en3d/damo/cv_3d-human-animation/3D-assets/blender-3.1.2-linux-x64/blender'

# Blender脚本的路径
blender_script_path = 'render_script.py'

file_path = 'action.gltf'

# 调用Blender命令行执行脚本
subprocess.run([blender_executable_path, '--background', '--python', blender_script_path, '--', file_path, str(120), './test'])
