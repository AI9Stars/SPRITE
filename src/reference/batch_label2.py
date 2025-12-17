import numpy as np
from PIL import Image,ImageDraw
from skimage.segmentation import find_boundaries
import json 
import os 
from tqdm import tqdm
import argparse

fill2color = {
    0:(0, 255, 0), ### green
    1:(0, 0, 255), ### blue
    2:(255, 0, 0), ### red
    3:(255,0,255), ### purple
    4:(255,255,0) ### yellow
}

def label_bound(npy_path,image_path,color_map,save_path):
    array = np.load(npy_path)
    pillow_img = Image.open(image_path)
    rgb_img = np.array(pillow_img)

    assert array.shape[:2] == rgb_img.shape[:2],"数组和图像尺寸不匹配{},{}".format(array.shape,rgb_img.shape)

    for key,value in color_map.items():
        candidate = int(key)
        one = (array == candidate).astype(np.uint16)
        if one.size < 5000:
            continue
        bound = find_boundaries(one, mode="thick")
        
        draw = ImageDraw.Draw(pillow_img)
        bound_coords = np.where(bound)  # 获取边界坐标（更高效写法）
        for y, x in zip(bound_coords[0], bound_coords[1]):
            draw.point((x, y), fill=fill2color[value])  

        pillow_img.save(save_path)



def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path",type = str)
    parser.add_argument("--npy_dir",type = str)
    parser.add_argument("--image_dir",type = str)
    parser.add_argument("--save_dir",type= str)
    args = parser.parse_args()

    return args 


if __name__ == "__main__":


    args = parse_args()
    input_path = args.input_path

    with open(input_path,"r",encoding = 'utf-8') as f:
        data_all = json.load(f)

    npy_dir_all = args.npy_dir
    image_dir_all = args.image_dir
    save_dir = args.save_dir


    for item in tqdm(data_all):
        scene = item["scene"].replace("_mate_info.json","")
        npy_dir = os.path.join(npy_dir_all,scene)
        image_dir = os.path.join(image_dir_all,scene)

        save_name = "{}_{}".format(scene,item["category"])

        if "/" in save_name:
            save_name = save_name.replace("/","-or-")
        output_dir = os.path.join(save_dir,save_name)
        if os.path.exists(output_dir) is not True:
            os.mkdir(output_dir)
        # print(len(item["color_map"]))
        for index in item["appear_all"]:
            npy_path = os.path.join(npy_dir,"frame_{}.npy".format(index))
            image_path = os.path.join(image_dir,"frame_{}.jpg".format(index))
            save_path = os.path.join(output_dir,"frame_{}.jpg".format(index))
            if os.path.exists(image_path):
                label_bound(npy_path,image_path,item["color_map"],save_path)

        

