PROMPTS = {}


PROMPTS["only"] = """
Please give an alias to the objects surrounded by bounding boxes in the following pictures. The bounding box colors of different objects are not the same, while those of the same object are the same.
The types of objects surrounded by bounding boxes are :{object}
The bounding box colors are :{color}
Aliases need to be given to {num} objects.
Note
The bounding box colors of different objects are not the same, while the bounding box colors of the same object are the same.
2. For aliases given to objects, please use 2 to 6 words to represent them
3. The alias requirement is a phrase
4. Objects can be distinguished by their aliases, and the aliases of each object cannot be the same.
5. The number of similar objects corresponds one-to-one with the number of bounding box colors.
6. Please present your responses in json format and refer to the following examples:
```json
{example}
```
"""

EXAMPLE = {
    "red":"Chair with a backrest",
    "green":"brown chair"
}