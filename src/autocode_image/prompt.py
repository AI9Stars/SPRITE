


PROMPTS = {}

PROMPTS["question"] = """
You are a teacher for an embodied task course, and your task is to create some test questions for an image based on the corresponding task type.
###Noted
1.The proposed test questions must only use the candidate object information provided by the user, especially the object names, which must correspond one-to-one. The candidate objects include the object names and their corresponding category information
This is the name of the candidate object and the corresponding type of the candidate object,The content is a dictionary, with the key being the object name and the value being the object type
### candidate object
```
{objects_info}
```
2.The proposed test questions require that they can be solved through code based on the meta information of the object.
The following is an example of metainformation. The object information in the example is not a candidate object
### meta information 
```
{meta_example}
```
The content and meaning are as follows:
id:The unique name of an object
obb:obb is three-dimensional OrientedboundingBox. In the coordinate system, the Y-axis is perpendicular to the ground and upward
    In obb information, "center" represents the centroid coordinate of an object in the world coordinate system
    "half_extent" is the half-length of the OBB, indicating the distance from the center point to each face
    "sizes" is the size of the OBB, indicating the length, width and height of the OBB.
    "volume" represents the size of the space occupied by OBB
"categoy" represents the type information of an object
In coordinate information, a movement of 0.1 unit is equivalent to 0.1 meter in reality
Additionally, the known extra information is the camera position:
camera_position = [-1.703, 0.985824, 0.922993]
The raised questions need to comply with the following task types and indicate the task types in the output results.
```
{question_type_all}
```
4.The proposed test questions need to explicitly include the name information of the object and the name of the task type.
5.The output needs to be in json format. The output example is as follows, and the question types can refer to the example:
```
{output_example}
```
instruction: Test question content
objcets:The names of the objects involved in the question are selected from the names of the candidate objects
objcets_category: what should be written here is the name of the object category
category:Task type
6.For numerical problems, units need to be included in the problem
7.For questions about object dimensions and the like, just ask about one dimension of length, width, and height in the question.
8.For a picture, please select the appropriate question type and ask at least 20 questions and the number of questions of different types should be as even as possible.
9.Please refer to the given picture and propose questions with practical significance.
"""




PROMPTS["code_generate"] = """
You are a senior engineer of python code. Your task is to write a function based on user questions, and the requirement is that the return result of the function is a string.
###Known information
1.The function name is func and the parameter passes a metadata variable and a camera_position variable. The function is defined as follows
```
def func(metadata,camera_position):
```
2.The content of metadata is a list. The following is part of the list. The content format is as follows. 
Please refer to the format. The specific content is passed by the metadata variable.
```
{meta_info}
```
The content and meaning are as follows:
id:The unique name of an object
obb:obb is three-dimensional OrientedboundingBox. In the coordinate system, the Y-axis is perpendicular to the ground and upward,The system follows the right-handed coordinate rule.
    In obb information, "center" represents the centroid coordinate of an object in the world coordinate system
    "half_extent" is the half-length of the OBB, indicating the distance from the center point to each face
    "sizes" is the size of the OBB, indicating the length, width and height of the OBB.
    "volume" represents the size of the space occupied by OBB
"categoy" represents the type information of an object
In coordinate information, a movement of 0.1 unit is equivalent to 0.1 meter in reality
3.The content of camera_position is a list. he content format is as follows. 
camera_position =  [-1.703,0.985824,0.922993]
###Noted
1.In the coordinate system, the Y-axis is perpendicular to the ground and upward,The system follows the right-handed coordinate rule.
2.The code part in the answer only needs to include the corresponding functions and there is no need to provide calling examples.
3.Please use the object names involved in the question when completing the code.
4.If it is a object_counting problem, what is counted is the number of objects of the same type, and the category of objects need to be used
5.The return result of the function must be a string and conform to the description in natural language
6.The output format can be referred to the reference code.
###reference code.
{reference_code}
###question
{question}
###The names of the objects involved in the question
{objects}
###The category of objects involved in the problem
{categories}
"""