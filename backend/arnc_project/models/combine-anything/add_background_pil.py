from PIL import Image
import numpy as np
import argparse
import os
import cv2


def parse_args( ):
    parser = argparse.ArgumentParser()
    parser.add_argument("--save_dir", type=str)
    parser.add_argument("--bg_mask_path", type=str)
    parser.add_argument("--bg_path", type=str)
    parser.add_argument("--frames", type=int)

    args = parser.parse_args()

    return args

def find_non_transparent_bounds(image):
    
    # 确保图像包含Alpha通道
    if image.mode in ('RGBA', 'LA'):
        # 将图像转换为NumPy数组
        image_array = np.array(image)
        
        # 获取Alpha通道
        alpha_channel = image_array[:, :, -1]
        
        # 找到非完全透明的像素
        non_transparent_pixels = np.where(alpha_channel != 0)
        
        # 计算非完全透明像素的边界
        top = np.min(non_transparent_pixels[0])
        left = np.min(non_transparent_pixels[1])
        bottom = np.max(non_transparent_pixels[0])
        right = np.max(non_transparent_pixels[1])
        
        return (left, top), (right, bottom)
    else:
        # 如果没有Alpha通道，则整个图像是不透明的
        return (0, 0), image.size


def find_nonzero_boundaries(image):
    # 加载图像并转换为灰度
    image = image.convert("L")
    
    # 将图像转换为NumPy数组
    image_array = np.array(image)
    
    # 寻找非零像素的坐标
    non_zero_indices = np.argwhere(image_array > 0)
    
    # 计算非零像素的最小和最大坐标
    top_left = non_zero_indices.min(axis=0)
    bottom_right = non_zero_indices.max(axis=0)
    
    # 返回边界（左上和右下角坐标）
    return (top_left[1], top_left[0]), (bottom_right[1], bottom_right[0])


if __name__ == '__main__':

    args = parse_args()

    # 调用函数并打印结果
    charac_path = os.path.join(args.save_dir, 'frame', '1.png')   # 替换为你的图像文件路径
    original_image = Image.open(charac_path)

    boundaries1 = find_non_transparent_bounds(original_image)
    # print(f"非透明像素的边界：左上角 {boundaries1[0]}, 右下角 {boundaries1[1]}")

    # back_mask_path = 'background/mask1.png'
    # back_mask = Image.open(back_mask_path)
    # boundaries2 = find_non_transparent_bounds(back_mask)
    # print(f"非透明像素的边界：左上角 {boundaries2[0]}, 右下角 {boundaries2[1]}")

    back_mask_path = args.bg_mask_path
    back_mask = Image.open(back_mask_path)
    boundaries2 = find_nonzero_boundaries(back_mask)
    print(f"非透明像素的边界：左上角 {boundaries2[0]}, 右下角 {boundaries2[1]}")


    # 新的高度, 这个计算方式有一点误差，应该影响不大
    new_height = int((boundaries2[1][1] - boundaries2[0][1]) / float((boundaries1[1][1] - boundaries1[0][1])) * original_image.size[1])
    print(new_height)

    # 计算新的宽度以保持宽高比
    height_percent = (new_height / float(original_image.size[1]))
    new_width = int((float(original_image.size[0]) * float(height_percent)))

    # 缩放图片
    resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)

    boundaries3 = find_non_transparent_bounds(resized_image)
    print(f"非透明像素的边界：左上角 {boundaries3[0]}, 右下角 {boundaries3[1]}")

    pointA = ((boundaries3[1][0] + boundaries3[0][0]) / 2.0, (boundaries3[1][1] + boundaries3[0][1]) / 2.0)

    pointB = ( (boundaries2[1][0] + boundaries2[0][0])/2.0 , (boundaries2[1][1] + boundaries2[0][1]) / 2.0)

    # 计算前景图片应该在背景图片上的位置
    position = (int(pointB[0] - pointA[0]), int(pointB[1] - pointA[1]))

    background_path = args.bg_path
    background = Image.open(background_path)

    # 使用paste方法覆盖图片，如果前景图片有透明通道，需要使用它作为mask
    background.paste(resized_image, position, resized_image)

    
    # 保存新的图片
    background.save(charac_path)

    start_frame = 2
    end_frame = args.frames

    for frame in range(start_frame, end_frame + 1):
        background = Image.open(background_path)
        
        
        img_path = os.path.join(args.save_dir, "frame", f"{frame}.png")
        img = Image.open(img_path)
        img = img.resize((new_width, new_height), Image.LANCZOS)

        background.paste(img, position, img)
        background.save(img_path)