
PROMPTS = {}


PROMPTS["complex_question"] = """
Below is a complex problem of reasoning, inference, please what is the complex problem.
Two simple questions were deduced during the reasoning process
Simple Question 1 :{A_Q} Answer :{A_A} Objects involved in the question :{A_O}
Simple Question 2 :{B_Q} Answer :{B_A} Objects involved in the question :{B_O}
Please infer this complex problem and provide the answer.
Note
This complex problem can definitely be answered based on simple questions and their answers.
2. If two objects have the same name, they are regarded as the same object.
3. Please output in json format. Refer to the json format example.
4. A complex problem is not a combination of two simple problems.
5. Here is an example:
Simple Question 1: How far is the distance between the table and the chair? Answer: 10m
Simple Question 2: What's on the table? Answer: A teacup
Based on the two simple questions and their answers given, I'll infer what this complex problem might be:
These two simple questions respectively obtained:
The distance between the table and the chair (10 meters)
What object is there on the table (a teacup)?
This information might be intended to solve a complex problem involving the positional relationships and states of these objects.
I infer that the complex problem might be:

```json

{example}

` ` `
"""

EXAMPLE = {
    "question":"If a person is sitting on a chair, can he get the teacup on the table?",
    "answer":"The distance between the table and the chair is 10. It's too far to reach the teacup on the table."
}

