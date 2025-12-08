

PROMPTS = {}


PROMPTS["question"] = """
There is currently a first-person video centered on the camera. 
Please create some test questions for the tasks in the embodied scenarios based on this video.
###Noted
1.The proposed test questions can only use the candidate object information provided by the user, especially the object name information needs to correspond one-to-one
This is the name of the candidate object and the corresponding type of the candidate object
### candidate object
```
{objects_info}
```
2.The proposed test questions require that they can be solved through code based on the meta information of the object.
### meta information 
```
{meta_example}
```
The content and meaning are as follows
id:The unique name of an object
obb:obb is three-dimensional OrientedboundingBox. In the coordinate system, the Y-axis is perpendicular to the ground and upward
    In obb information, "center" represents the centroid coordinate of an object in the world coordinate system
    "half_extent" is the half-length of the OBB, indicating the distance from the center point to each face
    "rotation" is a quaternion representing the rotation of the OBB.
    "sizes" is the size of the OBB, indicating the length, width and height of the OBB.
    "volume" represents the size of the space occupied by OBB
"categoy" represents the type information of an object
"appear" indicates in which pictures an object appears. For example, "appear = [0,1]" means it appears in the first and second pictures. The sequence of the pictures indicates the time information.
In coordinate information, a movement of 0.1 unit is equivalent to 0.1 meter in reality
3.The raised questions need to comply with the following task types and indicate the task types in the output results.
```
{question_type_all}
```
4.The proposed test questions need to explicitly include the name information of the object and the name of the task type.
5.The output needs to be in json format. The output example is as follows, and the question types can refer to the example:
```
{output_example}
```
instruction: Test question content
objcets:The names of the objects involved in the test questions, and the names of the objects involved must explicitly appear in the instruction. 
objcets_category: what should be written here is the name of the object category
category:Task type
6.For a video, please select an appropriate type of question. At least 40 questions should be raised, and the number of questions of different types should be as even as possible.
7.For questions about object dimensions and the like, just ask about one dimension of length, width, and height in the question.
8.The perspective position information in the video is unknown, so the perspective information should not be assumed in the test questions. When designing test questions about perspective transformation, three objects need to be included to determine their relative positions.
9.Please refer to the given video and propose a video with practical significance.
"""



PROMPTS["code_generate"] = """
You are a senior engineer of python code. Your task is to write a function based on user questions, and the requirement is that the return result of the function is a string.
###Known information
1.The function name is func and the parameter passes a metadata variable. The function is defined as follows
```
def func(metadata):
```
2.The content of metadata is a list. The following is part of the list. The content format is as follows. 
Please refer to the format. The specific content is passed by the metadata variable.
```
{meta_info}
```
The content and meaning are as follows
id:The unique name of an object
obb:obb is three-dimensional OrientedboundingBox. In the coordinate system, the Y-axis is perpendicular to the ground and upward
    In obb information, "center" represents the centroid coordinate of an object in the world coordinate system
    "half_extent" is the half-length of the OBB, indicating the distance from the center point to each face
    "rotation" is a quaternion representing the rotation of the OBB.
    "sizes" is the size of the OBB, indicating the length, width and height of the OBB.
    "volume" represents the size of the space occupied by OBB
"categoy" represents the type information of an object
"appear" indicates in which pictures an object appears. For example, "appear = [0,1]" means it appears in the first and second pictures. The sequence of the pictures indicates the time information.
In coordinate information, a movement of 0.1 unit is equivalent to 0.1 meter in reality
###Noted
1.The code part in the answer only needs to include the corresponding functions and there is no need to provide calling examples.
2.Please use the object names involved in the question when completing the code.
3.If it is a object_counting problem, what is counted is the number of objects of the same type, and the category of objects need to be used
4.The output format and code logic can be referred to the reference code.
###reference code.
{reference_code}
###question
{question}
###The names of the objects involved in the question
{objects}
###The category of objects involved in the problem
{categories}
"""