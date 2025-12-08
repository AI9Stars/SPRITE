

```
autocode_image/
├── few_shot/
│   └── ...
├── analyse.py              ### Analyze the model generation results to obtain the generated problems
├── exec_code.py            ### Execute the generated code
├── filter.py               ### Filter data through rules
├── generate_code.py        ### Generate code 
├── generate_ori.py         ### Sort out the original data
├── generate_question.py    ### Generate question code
├── model_api.py
├── model_qwen.py               
├── prompt_code.py          ### prompt for the answer
├── prompt.py               ### prompt for the question
└── verify_rule_1.py        ###  Verify the generated question

```


## Steps for generating questions
1. Centered on mateinfo, organize the resources required for a problem to form json generate_ori.py
2. Centered on mateinfo, generate questions through prompts and run generate_question.py
3. Parse and generate the problem analyse.py
4. Filter out issues such as incorrect number of selected objects and mismatch of object names through rules verify_rule1.py


## Steps for generating the answer
1. Proceed through qwen3-32B, design a prompt for processing, and obtain the answer. generate_code.py
2. Execute the code to obtain the answer: exex_code.py
3. Filter the answers according to the rules and remove the data whose answers are obviously problematic filter.py