from openai import OpenAI
import os 
import base64
from PIL import Image
from io import BytesIO
import json 
import os 
import numpy as np


class Model_Api():

    def __init__(self):

        self.model_type_gpt = "gpt-4o"

        self.client_dp = OpenAI(api_key="xxxx")

    def ask_model(self,data):

        try:
            response = self.client_dp.chat.completions.create(
                model = self.model_type_gpt, 
                messages = data,
                temperature = 1.0,
                )
            print(response.usage)
            return response.choices[0].message.content


        except Exception as e:
            print(e)
            return "执行出错"

    def encode_image(self,image_path):

        with Image.open(image_path) as img:
            # 调整图片分辨率
            resized_img = img.resize((256, 256), Image.Resampling.LANCZOS)
            
            # 将图片保存到BytesIO对象中
            buffered = BytesIO()
            resized_img.save(buffered, format="PNG")  # 可以根据需要更改格式，如PNG
            # 将BytesIO对象中的图片数据编码为Base64
            img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        return img_base64

    def encode_image2(self,image_path):

        with Image.open(image_path) as img:
            # 调整图片分辨率
            resized_img = img.resize((512, 512), Image.Resampling.LANCZOS)
            
            # 将图片保存到BytesIO对象中
            buffered = BytesIO()
            resized_img.save(buffered, format="PNG")  # 可以根据需要更改格式，如PNG
            # 将BytesIO对象中的图片数据编码为Base64
            img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        return img_base64

    def get_prompt_multi_image(self,prompt,image_dir):
        ### 生成处理多图的prompt 输入是文字和图片路径 图片要求是png格式
        content = [{"type": "text", "text": prompt}]
        image_all = os.listdir(image_dir)
        image_all = sorted(image_all,key=lambda x:int(x.split("_")[1].split(".")[0]))
        # print(image_all)
        for path in image_all:
            image_path = os.path.join(image_dir,path)
            base64_image = self.encode_image(image_path)
            t =  {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    }
                }
            content.append(t)
        messages=[
            {
                "role": "user",
                "content": content
            }
        ]
        return messages
    def get_promp_only_image(self,prompt,image_path):
        content = [{"type": "text", "text": prompt}]
        base64_image = self.encode_image2(image_path)
        t = {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    }
    
            }
        content.append(t)
        messages=[
            {
                "role": "user",
                "content": content
            }
        ]
        return messages

    def ask_model_only_image(self,prompt,image_path):
        messages = self.get_promp_only_image(prompt,image_path)
        response = self.ask_model(messages)

        return response
    
    def ask_model_muli_image(self,prompt,image_dir):
        messages = self.get_prompt_multi_image(prompt,image_dir)
        # response = ""
        response = self.ask_model(messages)

        return response