import json 

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
    


    for item in data_all:

        if item["category"] in ["object_abs_distance","object_size_estimation"]:

            if "meter" in item["instruction"]:
                continue 
            else:
                item["instruction"] = item["instruction"] + "Please answer in meters."
        elif item["category"] == "object_volume_estimation":
            if "meter" in item["instruction"]:
                continue
            else:
                item["instruction"] = item["instruction"] + "Please answer in cubic meters." 

    with open(output_path,"w",encoding = 'utf-8') as f:
        json.dump(data_all,f,ensure_ascii=False,indent=4)

        

