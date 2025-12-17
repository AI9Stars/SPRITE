import json 
import os 
from prompt import PROMPTS,EXAMPLE
from model_api import Model_Api
from tqdm import tqdm
from multiprocessing import Pool
# from model import Qwenvl
import argparse

fill2color = {
    0:(0, 255, 0), ### green
    1:(0, 0, 255), ### blue
    2:(255, 0, 0), ### red
    3:(255,0,255), ### purple
    4:(255,255,0) ### yellow
}

COLOR = ["green","blue","red","purple","yellow"]
def get_prompt(data):

    scene = data["scene"].replace("_mate_info.json","")
    image_path = "{}_{}".format(scene,data["category"])

    if "/" in image_path:
        image_path = image_path.replace("/","-or-")
    image_path = os.path.join(image_dir_all,image_path)

    ###all images 

    prompt_temp = PROMPTS["only"]
    object_category = data["category"]
    count = len(data["color_map"])
    color_all = ",".join(COLOR[:count])
    
    prompt = prompt_temp.format(object = object_category, num = count,color = color_all, example = EXAMPLE)

    return prompt,image_path


def cot_gen(data):

    try:
        prompt,image_path = get_prompt(data)
        # print(prompt)
        messages = client.get_prompt_multi_image(prompt,image_path)
    except Exception as e:
        print(e)
        response = "解析图片出错"
        d = {**data,"response":response}
        return d

    response = client.ask_model(messages,"4o")
    d = {**data,"response":response}
    return d


def CoT_gen_parallel(data,works_num = 5):       

    pool = Pool(works_num)
    x_y = tqdm(data)
    result = pool.map(cot_gen,x_y)

    return result

import argparse

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path",type = str)
    parser.add_argument("--image_dir",type = str)
    parser.add_argument("--output_path",type= str)
    args = parser.parse_args()

    return args 

if __name__ == "__main__":



    args = parse_args()
    input_path = args.input_path

    with open(input_path,"r",encoding = 'utf-8') as f:
        data_all = json.load(f)
    image_dir_all = args.image_dir
    output_path = args.output_path
    client = Model_Api()

    # data_all = data_all[:5]
    import time
    start_time = time.time() 

    instances = CoT_gen_parallel(data_all)

    end_time = time.time()  
    elapsed_time = end_time - start_time  

    print(f"耗时: {elapsed_time:.2f} 秒")  
    with open(output_path,"w",encoding = 'utf-8') as f:
        json.dump(instances,f,ensure_ascii=False,indent=4)
