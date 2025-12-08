import json 

###多线程的类
from multiprocessing import Pool
import argparse
from model_api import Model_Api
from prompt import PROMPTS

from tqdm import tqdm
import os 

def get_prompt(data):
    

    objects_info_path = os.path.join(objects_dir,data["metainfo_path"])
    with open(objects_info_path,"r",encoding = 'utf-8') as f:
        objects_info = json.load(f)
    prompt_temp = PROMPTS['question']
    prompt = prompt_temp.format(objects_info = objects_info,meta_example = meta_info_temp,question_type_all = question_type,output_example = question_temp)
    # print(prompt)
    return prompt

def Cot_gen(data):

    prompt = get_prompt(data)    
    image_path = os.path.join(image_dir,data["image_path"])
    # print(image_path)
    # print(prompt)
    try:
        response = client.ask_model_only_image(prompt,image_path)
    except:
        response = ""
    # print(prompt)
    # response = ""
    d = {**data,"response":response}
    return d

def CoT_gen_parallel(data,works_num = 5):       
    pool = Pool(works_num)
    x_y = tqdm(data)
    result = pool.map(Cot_gen,x_y)
    return result


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path",type = str)
    parser.add_argument("--image_dir",type = str )
    parser.add_argument("--objects_dir",type = str)
    parser.add_argument("--output_path",type= str)
    args = parser.parse_args()

    return args 

if __name__ == "__main__":


    args = parse_args()
    image_dir = args.image_dir
    objects_dir = args.objects_dir
    
    with open(args.input_path,"r",encoding= 'utf-8') as f:
        data_all = json.load(f)


    with open("few_shot/question_temp.json","r",encoding= 'utf-8') as f:
        question_temp = json.load(f)
    with open("few_shot/question_type.json","r",encoding= 'utf-8') as f:
        question_type = json.load(f)
    with open("few_shot/metainfo_temp.json","r",encoding= 'utf-8') as f:
        meta_info_temp = json.load(f)

    # data_all = data_all[:1]
    client = Model_Api()
    import time
    start_time = time.time() 
    instances = CoT_gen_parallel(data_all)
    end_time = time.time()  
    elapsed_time = end_time - start_time  
    print(f"耗时: {elapsed_time:.2f} 秒")  
    with open(args.output_path,"w",encoding='utf-8') as f:
        json.dump(instances,f,ensure_ascii=False,indent=4)


