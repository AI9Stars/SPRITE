from tqdm import tqdm
import json 

from prompt_code import PROMPT_CODE
from prompt import PROMPTS
from model_qwen import qwen_model
import random

def get_prompt(question):


    prompt_temp = PROMPTS["code_generate"]

    try:
        reference_code = PROMPT_CODE["object_direction_camera_complex"]
    except:
        return False
    content = prompt_temp.format(meta_info = str(meta_example), question= question["instruction"],
                                objects = str(question["objects"] ),categories = str(question["objects_category"] ), reference_code = reference_code)

    return content 

import argparse
def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path",type = str,help = "Input file path" )
    parser.add_argument("--output_path",type = str,help = "Output file path" )
    parser.add_argument("--model_path",type = str,help = "Model path" )
    args = parser.parse_args()

    return args 


if __name__ == "__main__":

    args = parse_args()
    input_path = args.input_path
    model_path = args.model_path
    output_path = args.output_path


    with open("few_shot/metainfo_temp.json","r",encoding = 'utf-8')  as f:
        meta_example = json.load(f)

    with open(input_path,"r",encoding = 'utf-8') as f:
        data_all = json.load(f)
    
    data_all = data_all[:40000]
    # random.shuffle(data_all)

    ###构造prompt
    prompts = []
    data_all_t = []
    for data in data_all:   
        t = get_prompt(data)
        if t is not False:
            prompts.append(t)
            data_all_t.append(data)
    llm = qwen_model(model_path = model_path)
    instances = []
    batch_size = 50
    print(len(data_all_t))

    prompts_batch = [prompts[i:i + batch_size] for i in range(0, len(prompts), batch_size)]
    data_all_t_batch =  [data_all_t[i:i + batch_size] for i in range(0, len(data_all_t), batch_size)]

    assert len(prompts) == len(data_all_t) 
    for index,prompt_batch in enumerate(tqdm((prompts_batch))):
        response = llm.generate_batch(prompt_batch)

        for item1,item2 in zip(data_all_t_batch[index],response):
            instances.append({**item1,"response":item2})

        with open(output_path,"w",encoding = "utf-8") as f:
            json.dump(instances,f,ensure_ascii = False ,indent = 4)