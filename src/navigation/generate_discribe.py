import json 

from model import Qwenvl

from tqdm import tqdm 
import os 
import ray
import parser

PROMPT = """
There is a camera that has carried out a series of movements in three-dimensional space. Now there is a series of pictures taken in chronological order along the path, as well as the general movement trajectory. Please refer to this information and describe the process of the camera from the starting point to the end point in navigation language.
Object movement trajectory
{path}
Note
The motion coordinates of an object are stored in chronological order.."
2. Please answer in English. When describing, you need to clearly describe which objects you pass by and be able to reach the corresponding positions based on the description.
3. Please describe the environment of the key nodes.
4. The reference motion trajectory contains numerical values. When describing, add numerical descriptions such as the camera rotation Angle and walking distance.
5. Please describe the process of the camera from its starting point to its destination in natural language
"""

ray.init()

@ray.remote(num_gpus=2)
def eval_model(data_all):

    model = Qwenvl(model_path = model_path)
    instances = []
    for item in tqdm(data_all):

        prompt = PROMPT.format(path = item["path_dis"])
        video_path = item["video_path"]
        response = model.generate_video(prompt,video_path)
        instances.append({**item,"response":response})
    return instances 


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path",type = str)
    parser.add_argument("--input_path",type = str)
    parser.add_argument("--output_path",type= str)
    args = parser.parse_args()

    return args 


if __name__ == "__main__":


    args = parse_args()
    input_path = args.input_path
    model_path = args.model_path
    output_path = args.output_path


    with open(input_path,"r",encoding="utf-8") as f:
        data_all = json.load(f)

    print(len(data_all))
    n_gpu = 8
    nums_all = 4
    chunks = [data_all[i::nums_all] for i in range(nums_all)]

    futures = [eval_model.remote(chunk) for chunk in chunks]

    results = ray.get(futures)
    final_results = []
    for result in results:
        final_results.extend(result)
    
    with open(output_path,"w",encoding="utf-8") as f:
        json.dump(final_results,f,ensure_ascii=False,indent=4)

    

