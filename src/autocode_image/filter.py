import json 
import re
import argparse
def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path",type = str,help = "Input file path" )
    parser.add_argument("--output_path",type = str,help = "Output file path" )
    args = parser.parse_args()

    return args 


if __name__ == '__main__':



    args = parse_args()
    input_path = args.input_path
    output_path = args.output_path
    with open(input_path,"r",encoding = 'utf-8') as f:
        data_all = json.load(f)


    instances = []

    for item in data_all:
        fuc_str = item.pop("response",None)
        code_res = item["code_res"]

        if len(code_res) == 0 or "unknow" in code_res or "无法" in code_res or code_res is None:
            continue

        if "invalid" in code_res:
            continue
        
        if "no" in code_res.lower() and "found" in code_res:

            continue

        if "[]" in code_res :
            continue

        if "_" in code_res:
            continue
        if isinstance(code_res,str) and len(code_res.split(",")) > 10:
            # print(code_res)
            continue
        if isinstance(code_res,str) and len(code_res.split(">")) > 10:
            continue
        
        if isinstance(code_res,str) and len(code_res.split(";")) > 10:
            continue
    

        fuc_str_analyse = re.findall(r"```python(.*?)```",fuc_str,re.DOTALL)
        ### 解析字符串
        if len(fuc_str_analyse) == 0:
            fuc_str = fuc_str
        else:
            fuc_str = fuc_str_analyse[0]
        item["respoonse"] = fuc_str
        instances.append(item)


    print(len(instances))

    with open(output_path,"w",encoding="utf-8") as f:
        json.dump(instances,f,ensure_ascii=False,indent=4)