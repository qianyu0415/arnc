from pygltflib import GLTF2

def convert_glb_to_gltf(input_glb_path, output_gltf_path):
    # 加载GLB文件
    gltf = GLTF2().load_binary(input_glb_path)
    
    # 保存为GLTF文件
    gltf.save_json(output_gltf_path)
    print(f"Converted {input_glb_path} to {output_gltf_path}")

# # 调用函数进行转换
# input_glb_path = "action.glb"
# output_gltf_path = "action.gltf"
# convert_glb_to_gltf(input_glb_path, output_gltf_path)
