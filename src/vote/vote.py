import requests
import json
import time
from tqdm import tqdm
import os



API_KEY = ""
API_URL = ""


def parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file_1",type = str)
    parser.add_argument("--input_file_2",type = str)
    parser.add_argument("--input_file_3",type = str)
    parser.add_argument("--output_path",type= str)
    args = parser.parse_args()

    return args 


def make_hashable(value):
    """将值转换为可哈希的类型"""
    if isinstance(value, list):
        # 递归处理嵌套列表
        return tuple(make_hashable(item) for item in value)
    elif isinstance(value, dict):
        # 递归处理嵌套字典
        return tuple(sorted((k, make_hashable(v)) for k, v in value.items()))
    else:
        return value
def get_openai_response(instruction,code1, code2, code3):
    url = API_URL
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
Your task is to determine whether three code snippets are functionally equivalent in expressing the answer to the same problem {instruction} (i.e., whether they convey the same meaning), ignoring non-functional differences such as comments, whitespace, variable names, etc.
The output should be a JSON object containing the judgment basis and a label.

以下是这三个代码片段：
<code1>
{code1}
</code1>

<code2>
{code2}
</code2>

<code3>
{code3}
</code3>

<Thought Process>
[Analyze whether the semantics of these three code snippets are consistent]
</Thought Process>

<Output Format>
{{
    "judgment_basis": "[Detailed judgment basis]",
    "label": [0 或 1]  # 0 indicates semantically inequivalent, 1 indicates semantically equivalent
}}
</Output Format>

Please ensure the analysis is objective and the output is in valid JSON format.
    """

    data = {
        "model": "gpt-4o-mini",
        "max_tokens": 16384,
        "messages": [
            {"role": "system", "content": "You are an expert in code semantic comparison."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            completion = response.json()
            return completion.get("choices")[0].get("message").get("content")
        else:
            print(f"API error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"API request failed: {str(e)}")
        return None


def compare_three_jsons(json_paths, output_path, max_retries=3):
    """
    :param json_paths: list, paths of 3 JSON files
    :param output_path: path of the output JSON file
    :param max_retries: maximum number of retries for failed API calls
    """
  
    datas = []
    for path in json_paths:
        try:
            with open(path, "r", encoding="utf-8") as f:
                datas.append(json.load(f))
            print(f"Successfully read file: {path}, containing {len(datas[-1])} items")
        except Exception as e:
            print(f"Failed to read file {path}: {str(e)}")
            return


    dicts = []
    for data in datas:
        id_dict = {}
        for item in data:
     
            key_value_pairs = []
            for k, v in item.items():
                if k in ['response', 'code_res']:
                    continue
         
                hashable_v = make_hashable(v)
                key_value_pairs.append((k, hashable_v))

            
            identifier = tuple(sorted(key_value_pairs))
            id_dict[identifier] = item
        dicts.append(id_dict)


    common_ids = set(dicts[0].keys())
    for d in dicts[1:]:
        common_ids &= set(d.keys())

    print(f"Number of common identifiers: {len(common_ids)}")

    results = []
    consistent_count = 0
    inconsistent_count = 0
    error_count = 0
    missing_count = 0

    # 创建进度条
    for identifier in tqdm(common_ids, desc="compare"):
        items = [d.get(identifier) for d in dicts]

 
        if not all('code_res' in item for item in items):
            missing_count += 1
            continue


        code_res_values = [item['code_res'] for item in items]

        # 尝试获取API响应
        json_response = None
        for attempt in range(max_retries):
            response_content = get_openai_response(
                items[0]['instruction'],
                code_res_values[0],
                code_res_values[1],
                code_res_values[2]
            )

            if response_content:
                try:
                    # 尝试解析JSON响应
                    json_response = json.loads(response_content)
                    break
                except json.JSONDecodeError:
                    print(f"JSON解析失败 (尝试 {attempt + 1}/{max_retries})")
                    if attempt < max_retries - 1:
                        time.sleep(2)  
                    else:
                        json_response = {
                            "judgment_basis": "Invalid API response format.",
                            "label": -1
                        }
            else:
                json_response = {
                    "judgment_basis": "API request failed.",
                    "label": -1
                }

        # 统计结果
        print(json_response)
        label = json_response.get("label", -1)
        if label == 1:
            consistent_count += 1
            results.append(items[0])  
        elif label == 0:
            inconsistent_count += 1
        else:
            error_count += 1

        
        time.sleep(1)

    #
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

   
    total_items = sum(len(d) for d in dicts)
    missing_count += total_items - 3 * len(common_ids)  #



    print(f"Total items: {total_items} | Common items: {len(common_ids)}")
    print(f"Consistent items: {consistent_count} | Inconsistent items: {inconsistent_count} | Error items: {error_count} | Missing items: {missing_count}")
    print(f"Consistency rate: {consistent_count / len(common_ids) * 100:.2f}%" if common_ids else "N/A")
    print(f"Results saved to: {output_path}")

    return results




# 示例用法
if __name__ == "__main__":

    args = parse_args()
    json_files = [
        args.input_file_1,
        args.input_file_2,
        args.input_file_3
    ]
        
    output_file = args.output_path

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    compare_three_jsons(
        json_paths=json_files,
        output_path=output_file
    )