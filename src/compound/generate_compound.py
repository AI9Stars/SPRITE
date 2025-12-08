from tqdm import tqdm
import json 
from prompt import PROMPTS,EXAMPLE
from openai import OpenAI

from multiprocessing import Pool
import argparse
def ask_model(data):

    try:

        response = client.chat.completions.create(
            model = "gpt-4o", 
            messages = data,
            temperature = 1.0,
            )
        # print(response.usage)
        text = response.choices[0].message.content
        return text

    except Exception as e:
        print(e)
        return "执行出错"

def get_prompt(question):


    prompt_temp = PROMPTS["complex_question"]
    content = prompt_temp.format(A_Q = question["question_a"]["instruction"],A_A = question["question_a"]["code_res"],A_O = str(question["question_a"]["objects"]),
                                B_Q = question["question_b"]["instruction"],B_A = question["question_b"]["code_res"],B_O = str(question["question_b"]["objects"]),
                                example = str(EXAMPLE))
    messages=[{"role": "user", "content": content}]
    return messages 


def cot_gen(data):

    prompt = get_prompt(data)    

    response = ask_model(prompt)
    d = {**data,"response":response}
    return d

def CoT_gen_parallel(data,works_num = 20):       

    pool=Pool(works_num)
    x_y = tqdm(data)
    result = pool.map(cot_gen,x_y)

    return result

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path",type = str )
    parser.add_argument("--output_path",type= str)
    args = parser.parse_args()

    return args 
if __name__ == "__main__":

    args = parse_args()
    input_path = args.input_path
    output_path = args.output_path
    
 
    with open(input_path,"r",encoding = 'utf-8') as f:
        data_all = json.load(f)
    
    client= OpenAI(api_key="xxxx")
    instances = []
    instances = CoT_gen_parallel(data_all)

    with open(output_path,"w",encoding = "utf-8") as f:
        json.dump(instances,f,ensure_ascii = False ,indent = 4)
