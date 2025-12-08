import json 
import re 

import argparse
def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path",type = str)
    parser.add_argument("--output_path",type= str)
    args = parser.parse_args()

    return args 
if __name__ == "__main__":

    args = parse_args()
    input_path = args.input_path
    output_path = args.output_path

    with open(input_path,"r",encoding = 'utf-8') as f:
        data_all = json.load(f)

    instances = []
    for item in data_all:
        text = item["response"]
        text = text.replace("\n","")
        t = re.findall(r"```json(.*?)```",text)

        if len(t) == 1:
            anaylse_res = t[0]
            try:
                res = json.loads(anaylse_res)
            except:
                anaylse_res = anaylse_res.replace("'","\"")
                try:
                    res = json.loads(anaylse_res)
                except:
                    res = "解析失败"


        else:
            # index = text.find("</think>")
            # t = text[index+8:]
            try:
                res = json.loads(text)
            except:
                res = "解析失败"

        instances.append({**item,"res":res})
    print(len(instances))
    with open(output_path,"w",encoding = "utf-8") as f:
        json.dump(instances,f,ensure_ascii = False ,indent = 4)
