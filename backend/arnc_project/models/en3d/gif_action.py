from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
from modelscope import snapshot_download
import os
import requests

if __name__ == '__main__':

    model_dir = snapshot_download('damo/cv_3d-human-animation', cache_dir='.')

    blender_path = os.path.join(model_dir, '3D-assets', 'blender-3.1.2-linux-x64', 'blender')

    file_path = './test/action_ids.txt'  # 根据需要调整路径
    with open(file_path, 'r') as file:
        action_list = file.read().splitlines()

    human3d = pipeline(Tasks.human3d_animation, model='damo/cv_3d-human-animation')

    for action in action_list:
        input = {'dataset_id': 'damo/3DHuman_synthetic_dataset', # character dataset, fixed
                'case_id': '200000', # character id, choose one from character dataset
                'action_dataset': 'damo/3DHuman_action_dataset', # action dataset, fixed
                'action': action, # action id, choose one from action dataset
                'save_dir': 'action_results',  # save directory,
                'blender': blender_path, # blender path
                }
        output = human3d(input)
        print(f'saved {action} file to {output}')

    print('finished!')
