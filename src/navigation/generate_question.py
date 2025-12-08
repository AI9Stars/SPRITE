import json 
import os 
import random 
import argparse 

from scripts import get_discribe

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--camera",type = str )
    parser.add_argument("--video_dir",type= str)
    parser.add_argument("--output_path",type= str)
    args = parser.parse_args()

    return args 

candidate_question = [
    "In this video, how can I move from the first frame to the last one?",
    "How do I go from the first frame to the last one in this video?",
    "How do I navigate from the first frame to the last frame in this video?",
    "How can I advance from the opening frame to the closing one in this video?",
    "How do I transition from the starting frame to the ending frame in this video?"
]

if __name__ == '__main__':

    args = parse_args()

    camera_dir = args.camera
    camera_all = os.listdir(camera_dir)
    video_dir = args.video_dir
    instances = []
    for camera in camera_all:
        
        scene = camera.replace("_points.json","")
        video_path = "{}.mp4".format(scene)
        video_path = os.path.join(video_dir,video_path)
        points_path = camera
        path_dis = get_discribe(os.path.join(camera_dir,camera))
        instruction = random.choice(candidate_question)


        d = dict(scene = scene,video_path = video_path,points_path = points_path,path_dis = path_dis,instruction = instruction)
        instances.append(d)

    with open(args.output_path,"w",encoding='utf-8') as f:
        json.dump(instances,f,ensure_ascii=False,indent=4)





