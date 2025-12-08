import json 
import re
import os 
from collections import defaultdict
import ast
from tqdm import tqdm
fill2color = {
    0:"green", ### green
    1:"blue", ### blue
    2:"red", ### red
    3:"purple", ### purple
    4:"yellow" ### yellow
}

def analyse(text):

    json_text = re.findall(r"```json(.*?)```",text,re.DOTALL)
    if len(json_text) == 0:
        return False
    json_text = json_text[0]

    try:
        res = json.loads(json_text)
    except:
        try:
            # 如果失败，尝试用ast.literal_eval解析（处理单引号的情况）
            return ast.literal_eval(json_text)
        except (ValueError, SyntaxError):
            # 如果都失败，抛出异常或返回None
            return False

    return res


import argparse

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path",type = str)
    parser.add_argument("--mate_info_dir",type = str)
    parser.add_argument("--save_dir",type= str)
    args = parser.parse_args()

    return args 

if __name__ == "__main__":


    args = parse_args()
    input_path = args.input_path

    with open("output/label_candidate_res.json","r",encoding = 'utf-8') as f:
        data_all = json.load(f)


    all_scene = defaultdict(list)

    for item in data_all:
        all_scene[item["scene"]].append(item)
    
    mate_info_dir = args.mate_info_dir
    save_dir = args.save_dir
    for key,value in tqdm(all_scene.items()):

        mate_info_path = os.path.join(mate_info_dir,key)

        with open(mate_info_path,"r",encoding='utf-8') as f:
            mate_info = json.load(f)

        ### 统计个数唯一的物体 将id改为category
        objects_count = defaultdict(int)

        for item in mate_info:
            objects_count[item["category"]] +=1
        ###分析response 
        mate_info_t = []
        all_objects = {}
        for object_t in value:

            response = analyse(object_t["response"])
            # print(response)
            if response is False:
                continue
            color_map_t = object_t["color_map"]
            d = {}
            try:
                for a,b in color_map_t.items():
                    d[a] = response[fill2color[b]]
            except:
                d = {}
                print(response)
                print(object_t["color_map"])
            all_objects.update(d)

        # print(all_objects)
        mate_info_t = []
     
        for item in mate_info:
            if str(item["semantic_id"]) in all_objects.keys():
                item["id"] = all_objects[str(item["semantic_id"])].lower()
            if objects_count[item["category"]] == 1:
                item["id"] = item["category"]
            if any(char.isdigit() for char in item["id"] ):
                continue 
            mate_info_t.append(item)
   
        output_path = os.path.join(save_dir,key)
        with open(output_path,"w",encoding = 'utf-8') as f:
            json.dump(mate_info_t,f,ensure_ascii=False,indent=4)

        # break
