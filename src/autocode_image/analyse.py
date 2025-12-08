
import json 
import re
import argparse

def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path",type = str,help = "Input file path" )
    parser.add_argument("--output_path",type = str,help = "Output file path" )
    args = parser.parse_args()

    return args 
def analyse_question(data):


    response = data.pop("response","")


    instances = []
    if not isinstance(response,str):
        return []
    ###正则
    t = re.findall(r"```json(.*?)```",response,re.DOTALL)
    if len(t)!=0:
        response = t[0]

    try:
        
        quesitons = json.loads(response)
    
        for item in quesitons:
            instances.append({**data,**item})
    except Exception as e:
        print(e)

        return []

    return instances


if __name__ == "__main__":


    with open(input_path,"r",encoding = 'utf-8') as f:
        data = json.load(f)

    # data = data[:5]
    instances = []
    for item in data:
        instances = instances + analyse_question(item)
    print(len(instances))
    with open(output_path,"w",encoding = "utf-8") as f:
        json.dump(instances,f,ensure_ascii = False ,indent = 4)



    