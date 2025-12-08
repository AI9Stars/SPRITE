import json 
import random
import itertools

def generate_question(data:list):

    objects = {}

    for index,item in enumerate(data):
        for obj in item["objects"]:

            if obj not in objects.keys():
                objects[obj] = set([index])
            else:
                objects[obj].add(index)

    # print(objects)
    response = set()
    for key,value in objects.items():
        ### 随机选
        if len(value)<2:
            continue
        
        
        response.update( list(itertools.combinations(list(value), 2)))

    instances = []
    for item in response:
        scene = data[0]["scene"]
        objects_path = data[0]["objects_path"]
        rgb_dir = data[0]["rgb_dir"]
        question_a = dict(instruction = data[item[0]]["instruction"],objects = data[item[0]]["objects"],category = data[item[0]]["category"],code_res =data[item[0]]["code_res"],objects_category =data[item[0]]["objects_category"])
        question_b = dict(instruction = data[item[1]]["instruction"],objects = data[item[1]]["objects"],category = data[item[1]]["category"],code_res =data[item[1]]["code_res"],objects_category =data[item[1]]["objects_category"]])

        d = dict(scene = scene,objects_path = objects_path,rgb_dir = rgb_dir,question_a = question_a,question_b = question_b)

        instances.append(d)
    
    return instances



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


    with open(input_path,"r",encoding = "utf-8") as f:
        data_all = json.load(f)


    scene_question = {}

    for item in data_all:
        if item["scene"] not in scene_question.keys():
            scene_question[item["scene"]] = [item]
        else:
            scene_question[item["scene"]].append(item)

    random.seed(42)
    instances = []
    for key,value in scene_question.items():

        t = generate_question(value)
        instances = instances + t

    print(len(instances))
    with open(output_path,"w",encoding = 'utf-8') as f:
        json.dump(instances,f,ensure_ascii=False,indent=4)


