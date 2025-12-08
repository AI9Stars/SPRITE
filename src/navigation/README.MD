

```
navigation/
├── generate_discribe.py            ### Generate path descriptions through code
├── generate_question.py            ### Polish the description of code generation
├── model_api.py
├── model.py
├── prompt.py
├── README.MD
└── scripts.py                      ### Code generation path description script
```

## Steps
1. Describe according to the camera position and the rules, generate the overall description question at the same time, and generate the answer through code generate_question.py
2. Polish the description of code generation through prompts. generate_discribe.py


Currently, the code defaults to using qwen2.5-vl as the base model to generate path descriptions. The code also provides the use of the closed-source model api to generate path descriptions.