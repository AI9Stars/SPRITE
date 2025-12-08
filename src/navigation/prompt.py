PROMPTS = {}


PROMPTS["navigation"] = """
There is a camera that has performed a series of movements in three-dimensional space. Now there is a series of pictures taken in chronological order along the path, as well as the approximate movement trajectory.
Please refer to this information to generate questions and answers that can enhance the model's navigation ability.
### movement trajectory.
{path_dis}
### notes
1. The questions generated should reflect navigation information, such as whether to turn left or right when arriving at a certain place.
2. Please answer in json format. Meanwhile, please refer to the example for the content of your answer. Each question needs to contain the corresponding answer.
3. Please raise at least 10 questions.The questions should be as diverse as possible.
### example
```
{example}
```
"""

PROMPT_EXAMPLE = [
    {
        "question":"I am beginning at the door and facing the stool. I want to navigate to the bed.How should I go? ",
        "answer":"Move straight ahead until you reach the stool, turn right, then continue forward until the bed, where you’ll arrive at the final destination"
    },
    {
        "question":"As you follow the path later, is there a moment when you should make a left turn to stay on course? ",
        "answer":"Yes, make a left turn after moving forward for a while."
    }
]