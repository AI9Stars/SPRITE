import json 
import os 
from tqdm import tqdm

OBJECTS2NUM = {
    "object_appearance_order":1,
    "object_abs_distance":1,
    "object_counting":2,
    "object_rel_distance":1,
    "object_size_estimation":1,
    "object_direction_facing_complex":1,
    "object_volume_comparison":1,
    "object_in_frame":1,
    "object_volume_estimation":1,
    "object_height_determination":1,
    "temporal_appearance_sequence":1,
    "object_nearby":1,
    "object_direction_facing_simple":1,
    "object_below":1,
    "object_above":1,
    "High_and_low_position":1

}
import argparse

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path",type = str)
    parser.add_argument("--objects_dir",type = str )
    parser.add_argument("--output_path",type= str)
    args = parser.parse_args()

    return args 

if __name__ == "__main__":


    args = parse_args()

    with open(args.input_path,"r",encoding = 'utf-8') as f:
        data_all = json.load(f)

# '''
# 通过规则进行过滤
# 1. 按照问题类型，物体数量进行过滤
# 2. 过滤掉问题中涉及物体 名称不对的情况
# 通过模型进行过滤
# 1. 问题是否合理 如问题中是否涉及无意义的物体
# 2. 涉及长度估计的问题，检查是否有单位，如无单位需要补全。
# '''
    objects_info_dir = args.objects_dir

    instances = []
    for item in tqdm(data_all):

        objects_path = item["objects_path"]
        objects_path = os.path.join(objects_info_dir,objects_path)

        with open(objects_path,"r",encoding = 'utf-8') as f:
            objects = json.load(f)
        flag = True
        if "objects" not in item.keys():
            # print(item)
            continue 
        for obj in item["objects"]:
            if objects.get(obj,None) is None:
                # print(obj)
                flag = False
                break 
        if flag is False:
            continue 
        

        ### 分类不正确
        try:
            objects_num = OBJECTS2NUM.get(item["category"],-1)
        except:
            # print(item)
            continue
        if objects_num == -1:
            continue
        

        ### 物体数量不正确
        if objects_num == 1:
            for obj in item["objects"]:
                if objects[obj] != objects_num:
                    flag = False
                    break 

        if flag is False:
            continue 
        instances.append(item)

    print(len(instances))
    with open(args.output_path,"w",encoding = 'utf-8') as f:
        json.dump(instances,f,ensure_ascii=False,indent=4)

        


        

        



