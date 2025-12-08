import json 
import os 
import argparse

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path",type = str)
    parser.add_argument("--objects_dir",type = str)
    parser.add_argument("--output_path",type= str)
    args = parser.parse_args()

    return args 

if __name__ == '__main__':


    args = parse_args()

    with open(args.input_path,"r",encoding = 'utf-8') as f:
        data_all = json.load(f)

    objects_dir = args.objects_dir
    print(len(data_all))
    instances = []
    for item in data_all:


        objects_path = os.path.join(objects_dir,item["metainfo_path"])

        with open(objects_path,"r",encoding = 'utf-8') as f:
            objects_data = json.load(f)
        if "objects_category" not in item.keys():
            continue
        flag = True
        for t in item["objects"]:
            if t not in objects_data.keys():
                flag = False
                break
        if flag:
            instances.append(item)
    
    print(len(instances))
    with open(args.output_path,"w",encoding = 'utf-8') as f:
        json.dump(instances,f,ensure_ascii=False,indent=4)

        
    