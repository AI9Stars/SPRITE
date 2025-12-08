from vllm import LLM,SamplingParams
from transformers import AutoTokenizer
import json 
from tqdm import tqdm
class qwen_model:

    def __init__ (self,model_path):

        self.tokenizer = AutoTokenizer.from_pretrained(model_path,trust_remote_code = True)
        self.model = LLM(model_path,trust_remote_code = True,max_model_len = 32786,tensor_parallel_size = 4)
        self.samplingparams = SamplingParams(temperature=0.7,max_tokens = 32786)
        print("加载模型完成")

    def generate_batch(self,prompts,think = True):

        all_text = []

        for item in prompts:

            messages = [{"role": "user", "content": item}]
            text = self.tokenizer.apply_chat_template(messages,tokenize=False,add_generation_prompt=True,enable_thinking=think)
            all_text.append(text)

        
        response = self.model.generate(all_text,self.samplingparams)

        # print(response)
        # import pdb;pdb.set_trace()
        outputs = [item.outputs[0].text  for item in response]
    
        return outputs
    

    def generate_batch_all(self,prompts,batch_size = 500):

        prompts_batch = [prompts[i:i + batch_size] for i in range(0, len(prompts), batch_size)]
        response = []
        for prompt_batch in tqdm(prompts_batch):
            response = response + self.generate_batch(prompt_batch)
        return response
