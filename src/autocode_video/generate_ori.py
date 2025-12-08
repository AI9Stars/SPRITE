import json 
import os  
import argparse 



def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--meta_info",type = str)
    parser.add_argument("--output_path",type= str)
    args = parser.parse_args()

    return args 


if __name__ == '__main__':

    args = parse_args()

    meta_info = args.meta_info
    meta_info_all = os.listdir(meta_info)

    instances = []
    for item in meta_info_all:
        
        scene = item.replace(".json","")
        # scene = item.replace("_mate_info.json","").replace(".json","")
        rgb_dir = scene
        objects_path = item
        meta_info_path = item

        d = dict(scene = scene,rgb_dir = rgb_dir,objects_path = objects_path,meta_info_path = meta_info_path)
        instances.append(d)
    print(len(instances))
    with open(args.output_path,"w",encoding='utf-8') as f:
        json.dump(instances,f,ensure_ascii=False,indent=4)





