import os
import imageio
from modelscope.pipelines import pipeline
from modelscope import snapshot_download
from modelscope.utils.constant import Tasks
from modelscope.outputs import OutputKeys
from modelscope.models.cv.face_reconstruction.utils import write_obj
import requests

model_dir = snapshot_download('damo/cv_3d-human-animation', cache_dir='.')
# install blender
blender_file = os.path.join(model_dir, '3D-assets', 'blender-3.1.2-linux-x64.tar.xz')
blender_path = os.path.join(model_dir, '3D-assets', 'blender-3.1.2-linux-x64', 'blender')
if not os.path.exists(blender_file):
    raise Exception('found blender file failed.')
if not os.path.exists(blender_path):
    cmd = f'tar -xvf {blender_file} -C {os.path.join(model_dir, "3D-assets")}'
    os.system(cmd)

def list_from_url(url):
    r = requests.get(url)
    list = r.content.decode('utf-8').split('\n')
    list = list[:-1]
    return list

def save_results(result, save_root):
    os.makedirs(save_root, exist_ok=True)

    # save mesh
    mesh = result[OutputKeys.OUTPUT]['mesh']
    write_obj(os.path.join(save_root, 'mesh.obj'), mesh)

    # save rendered color video
    frames_color = result[OutputKeys.OUTPUT]['frames_color']
    imageio.mimwrite(os.path.join(save_root, 'render_color.gif'), frames_color, duration=30)
    del frames_color

    # save rendered normals video
    frames_normals = result[OutputKeys.OUTPUT]['frames_normal']
    imageio.mimwrite(os.path.join(save_root, 'render_normals.gif'), frames_normals, duration=30)
    del frames_normals
    print(f'Output written to {os.path.abspath(save_root)}')


if __name__ == "__main__":
    human3d = pipeline(Tasks.human3d_render, model='damo/cv_3d-human-synthesis-library')

    url = 'https://modelscope.cn/api/v1/datasets/damo/3DHuman_synthetic_dataset/repo?Revision=master&FilePath=character_ids.txt'
    charac_id_list = list_from_url(url)

    for character in charac_id_list:
        input = {'dataset_id': 'damo/3DHuman_synthetic_dataset',  # 3dhuman-syn dataset, fixed
             'case_id': character,  # character id
             'resolution': 1280,  # render resolution
             }

    
    output = human3d(input)
    save_results(output, './human3d_results')
    print('download and render finished!')

    # # character ids of 3DHuman-Syn Dataset
    # url = 'https://modelscope.cn/api/v1/datasets/damo/3DHuman_synthetic_dataset/repo?Revision=master&FilePath=character_ids.txt'
    # charac_id_list = list_from_url(url)
    # print('character id list:', charac_id_list)

    action3d = pipeline(Tasks.human3d_animation, model='damo/cv_3d-human-animation')
    input = {'dataset_id': 'damo/3DHuman_synthetic_dataset', # character dataset, fixed
             'case_id': '000084', # character id, choose one from character dataset
             'action_dataset': 'damo/3DHuman_action_dataset', # action dataset, fixed
             'action': 'SwingDancing', # action id, choose one from action dataset
             'save_dir': 'human3d_results',  # save directory,
             'blender': blender_path, # blender path
             }
    output = action3d(input)
    print('saved animation file to %s' % output)
    print('finished!')






