
```
compound/
├── analyse.py                     ### Analyze the model generation results to obtain the generated problems
├── generate_compound.py           ### generate compound quesitons
├── prompt.py                      ### prompt for the question
└── select_question.py             ### Select two subquestions involving the same object as candidates
```



## steps
1. Select two subquestions involving the same object as candidates, select_question.py
2. Generate the compound questuons and answer through prompt generaate_compound.py 
3. Analyze the compound problem in analyse.py
