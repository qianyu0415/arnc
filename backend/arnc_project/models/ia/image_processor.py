import torch
import numpy as np
import os
from pathlib import Path
from rembg import remove
from sam_segment import predict_masks_with_sam_box, predict_masks_with_sam
from lama_inpaint import inpaint_img_with_lama
from utils import load_img_to_array, save_array_to_img, dilate_mask

def process_image_rembg(input_img, dilate_kernel_size, output_dir, sam_model_type, sam_ckpt, lama_config, lama_ckpt):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    img, image = load_img_to_array(input_img)

    # 使用rembg移除背景
    img_rem = image.convert('RGBA')
    img_nobg = remove(img_rem, alpha_matting=True)
    
    # 获取无背景图像的alpha通道作为遮罩
    arr = np.asarray(img_nobg)[:, :, -1]

    # 计算遮罩的边界框
    x_nonzero = np.nonzero(arr.sum(axis=0))
    y_nonzero = np.nonzero(arr.sum(axis=1))
    bbox = np.array([x_nonzero[0].min(), y_nonzero[0].min(), x_nonzero[0].max(), y_nonzero[0].max()])

    # 使用SAM模型生成遮罩
    masks, _, _ = predict_masks_with_sam_box(
        img,
        bbox,
        model_type=sam_model_type,
        ckpt_p=sam_ckpt,
        device=device
    )
    masks = masks.astype(np.uint8) * 255

    # 膨胀遮罩
    if dilate_kernel_size is not None:
        masks = [dilate_mask(mask, dilate_kernel_size) for mask in masks]

    # 保存遮罩和处理后的图像
    img_stem = Path(input_img).stem
    mask_path = os.path.join( output_dir, 'mask', img_stem +'.png')
    
    # processed_img_paths = []

    mask = masks[-1]

    save_array_to_img(mask, mask_path)

    img_inpainted = inpaint_img_with_lama(img, mask, lama_config, lama_ckpt, device=device)

    bg_path = os.path.join( output_dir, 'bg', img_stem + '.png')

    save_array_to_img(img_inpainted, bg_path)



    # #这段代码可以被优化，不需要创建三张图片其实
    # for idx, mask in enumerate(masks):
    #     mask_path = out_dir_path / f"mask_{idx}.png"
    #     save_array_to_img(mask, mask_path)

    #     # 使用LaMa模型进行图像修复
    #     img_inpainted = inpaint_img_with_lama(
    #         img, mask, lama_config, lama_ckpt, device=device)
        
    #     inpainted_img_path = out_dir_path / f"inpainted_{idx}.png"
    #     save_array_to_img(img_inpainted, inpainted_img_path)

    #     processed_img_paths.append(str(inpainted_img_path))

    # 返回处理后的第一张图像的路径作为示例
    # return processed_img_paths[2] if processed_img_paths else None

    return bg_path


def process_image(image, point_coords, point_labels, sam_model_type, sam_ckpt_path, lama_config_path, lama_ckpt_path, output_path, filename):
    
    img_array , _ = load_img_to_array(image)
    point_coords = list(map(int, point_coords.split(',')))
    point_labels = [int(label) for label in point_labels.split(',')]
    masks, _, _ = predict_masks_with_sam(img_array, [point_coords], point_labels, model_type=sam_model_type, ckpt_p=sam_ckpt_path, device='cuda')
    masks = masks.astype(np.uint8) * 255
    masks = [dilate_mask(mask, 15) for mask in masks]

    img_inpainted = inpaint_img_with_lama(img_array, masks[-1], lama_config_path, lama_ckpt_path, device='cuda')

    mask_path = os.path.join(output_path, 'mask', filename)
    mask = masks[-1]
    save_array_to_img(mask, mask_path)

    # inpainted_img_path = os.path.join(output_path , "inpainted_point.png")
    inpainted_img_path = os.path.join(output_path, 'bg',filename)
    save_array_to_img(img_inpainted, inpainted_img_path)

    return inpainted_img_path