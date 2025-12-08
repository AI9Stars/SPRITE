import os 
import json 

import argparse
def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir",type = str )
    parser.add_argument("--output_path",type = str )
    args = parser.parse_args()

    return args 

if __name__ == '__main__':



    args = parse_args()
    source_image_dir = args.input_dir

    all_images = os.listdir(source_image_dir)
    instances = []
    for item in all_images:
        index = item.rfind("frame_")
        pos = item[index:]
        # print(pos)
        scene = item[:index-1]
        pos = pos.replace("frame_","").replace(".jpg","")
        metainfo_path = item.replace(".jpg",".json")

        d = dict(scene = scene,image_path = item,pos = pos,metainfo_path = metainfo_path)

        instances.append(d)
      

    print(len(instances))
    with open(args.output_path,"w",encoding='utf-8') as f:
        json.dump(instances,f,ensure_ascii=False,indent=4)
