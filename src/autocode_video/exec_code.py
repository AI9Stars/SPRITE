import json 
import re 
import tempfile
import importlib.util
import os 
from tqdm import tqdm 

import argparse
def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path",type = str,help = "Input file path" )
    parser.add_argument("--meta_info_dir",type = str,help = "Meta Information Dir" )
    parser.add_argument("--output_path",type = str,help = "Output file path" )
    args = parser.parse_args()

    return args 

if __name__ == "__main__":


    args = parse_args()
    input_path = args.input_path
    output_path = args.output_path
    with open(input_path,"r",encoding = 'utf-8') as f:
        question_code = json.load(f)

    # question_code = question_code[:]
    exec_acc = 0
    code_err = 0
    instances = []
    print(len(question_code))
    meta_info_dir = args.meta_info_dir
    for index,item in tqdm(enumerate(question_code)):
        # print(index)
        meta_info_path = item["meta_info_path"]
        # print(meta_info_path)

        meta_info_path = os.path.join(meta_info_dir,meta_info_path)
        with open(meta_info_path,"r",encoding = "utf-8") as f:
            meta_info = json.load(f)

        fuc_str = item["response"]

        # fuc_str_answer = re.findall(r"<answer>(.*?)</answer>",fuc_str,re.DOTALL)
        index = fuc_str.find("</think>")
        fuc_str_answer = fuc_str[index+8:]
        # if len(fuc_str_answer) == 0:
        #     continue
        # fuc_str_answer = fuc_str_answer[0]
        fuc_str_analyse = re.findall(r"```python(.*?)```",fuc_str_answer,re.DOTALL)
        ### 解析字符串
        if len(fuc_str_analyse) == 0:
            fuc_str = fuc_str_answer
        else:
            fuc_str = fuc_str_analyse[0]
    
        ###排除掉有输入的情况
        if "input" in fuc_str or "read" in fuc_str or "__doc__" in fuc_str:
            code_err+=1
            continue
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as temp_file:
                temp_file.write(fuc_str)
                temp_file_path = temp_file.name
            module_name = "temp_module"
            spec = importlib.util.spec_from_file_location(module_name, temp_file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

        except  Exception as e :
            code_err +=1 
            continue
        if hasattr(module, "func"):
            func = module.func
            try:
                result = func(meta_info)
                exec_acc +=1
            except Exception as e:
                # print(item["instruction"])
                # print(fuc_str)
                code_err +=1
                continue
        else:
            code_err+=1
            continue
        item["response"] = fuc_str
        instances.append({**item,"code_res":str(result)})

    print(f"exec_acc:{exec_acc}\ncode_err:{code_err}")

    with open(output_path,"w",encoding="utf-8") as f:
        json.dump(instances,f,ensure_ascii=False,indent=4)
