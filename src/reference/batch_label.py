# import numpy as np
# from PIL import Image,ImageDraw
# from skimage.segmentation import find_boundaries
import json 
import os 
from collections import defaultdict
import random 
from tqdm import tqdm
import parser

def select_elements_from_list(lst):
    n = len(lst)
    if n <=5:
        return lst 
    
    t = random.sample(lst,5)
    
    return t 

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--mateinfo_dir",type = str)
    parser.add_argument("--output_path",type= str)
    args = parser.parse_args()

    return args 


if __name__ == "__main__":

    ### 1.从mateinfo的角度出发，对mate_info中的物体进行统计，同时生成一个映射文件 某个物体映射成什么颜色 对appear进行处理，选取图片
    ### 2.根据生成的映射文件 对图片进行标注
    ### 3.以标注好的图片为中心，通过4o生成
    ### 4.对生成结果进行处理，构造最后的mateinfo

    args = parse_args()
    
    random.seed(42)
    
    mateinfo_dir_all = args.mateinfo_dir

    mateinfo_all = os.listdir(mateinfo_dir_all)
    instances = []
    for item in tqdm(mateinfo_all):

        mate_info_path = os.path.join(mateinfo_dir_all,item)

        with open(mate_info_path,"r",encoding = 'utf-8') as f:
            mate_info = json.load(f)

        objects_all = defaultdict(list)
        for mm in mate_info:

            objects_all[mm["category"]].append(mm)

        instances_t = []
        for key,value in objects_all.items():
            if len(value)>=2 and len(value)<= 5:
                d = {}
                appear = []
                objects_selected = []
                color_map = {}
                for index, mate_t in enumerate(value):
                    appear = appear + select_elements_from_list(mate_t["appear"])
                    # objects_selected.append({"id":mate_t["id"],"category":mate_t["category"],"semantic_id":mate_t["semantic_id"],"appear":mate_t["appear"]})
                    color_map[str(mate_t["semantic_id"][0])] = index
                # d["objects"] = objects_selected
                d["appear_all"] = list(set(appear))
                d["scene"] = item
                d["category"] = key
                d["color_map"] = color_map
                instances_t.append(d)

            
            
        instances = instances + instances_t

        break 

    print(len(instances))
    with open(args.output_path,"w",encoding = 'utf-8') as f:
        json.dump(instances,f,ensure_ascii=False,indent=4)

    