from scripts.gpt_api import get_response_4v, get_response_new


# 使用GPT-4V 根据场景和物体信息生成文本化描述
def scene_to_description(file_path, scene_object_info, ego_object_info):
    photo_path = [f"{file_path}/photo_{i}.png" for i in range(4)]  # 图像路径
    prompt = ""
    prompt += "Imagine you are an embodied robotic assistant and you are in a virtual cartoon-style indoor scene. \n"
    prompt += "In this indoor scene there are the following objects: "
    for object_name, object_num in scene_object_info.items():
        prompt += f"{object_num} {object_name}, "
    prompt += ". \n"
    prompt += "These four images are from your first perspective of the scene, and the first image is from your front. \n"
    prompt += "Please combine these four images with the object information in the scene I gave you, and use natural language to describe the scene in detail for me, especially the characteristics and positional relationships of the objects in the scene. \n"
    prompt += "Examples are as follows: \n"
    prompt += "There is a wooden table in the scene with a red cup and a green toy car on the table. Next to the toy car is a black box with two pencils inside. There are chairs on each side of the wooden table. \n"
    prompt += "Note that you need to combine the contents of these four images to describe the scene, rather than analyzing each image separately. \n"

    scene_description = get_response_4v(photo_path, prompt, local=True)

    print("\n\n" + prompt + "\n\n")

    return scene_description


# 使用GPT-4 根据场景描述和任务模板生成任务
def description_to_task(scene_description, scene_object_info):
    prompt = ""
    prompt += "Suppose you are an embodied robotic assistant and you are in an indoor scene. The scene is described as follows: \n"
    prompt += scene_description
    prompt += " \n"
    prompt += "Taking into account the uncertainty of language description, it is clearly stated that there are a total of the following objects in the entire scene: "
    for object_name, object_num in scene_object_info.items():
        prompt += f"{object_num} {object_name}, "
    prompt += ". \n"
    prompt += "You need to help me complete a series of tasks. The task template is as follows: \n"
    prompt += "1.Is there a {object} in the scene? Where object is a specific object in the scene. \n"
    prompt += "2.What is the name of the object {postion}? Where position is a specific location in the scene, such as on the table. \n"
    prompt += "3.What is the object next to the {object}? Where object is a specific object in the scene. \n"
    prompt += (
        "4.What color is {object}? Where object is a specific object in the scene. \n"
    )
    prompt += "5.What is the shape of {object}? Where object is a specific object in the scene. \n"
    prompt += "6.Identify all the {color} objects in the room. Where color is a specific color. \n"
    prompt += "7.Where is {object}? Where object is a specific object in the scene. \n"
    prompt += "8.Go to {object}. Where object is a specific object in the scene. \n"
    prompt += "9.Move {object} to {position}. Where position is a specific location in the scene, such as on the table. \n"
    prompt += "10.Move {object1} closer/further to {object2}. Where object1 and object2 are specific objects in the scene. \n"
    prompt += "11.Put {object1} on the {object2}. Where object1 and object2 are specific objects in the scene. \n"
    prompt += "12.Pick up {object}. Where object is a specific object in the scene. \n"
    prompt += "13.Swap the positions of {object1} and {object2}. Where object1 and object2 are specific objects in the scene. \n"
    prompt += "14. Collect {object1, object2, ...} into {object0}. Where object1 and object2 are specific objects in the scene. \n"
    prompt += "15.Arrange {object1, object2, ...} in a line. Where object1 and object2 are specific objects in the scene. \n"
    prompt += "16.Arrange {object1, object2, ...} in a circle. Where object1 and object2 are specific objects in the scene. \n"
    prompt += "17.Remove {object1, object2, ...} from {object0}. Where object1 and object2 are specific objects in the scene. \n"
    prompt += "18.Clear the {position} of all objects. Where position is a specific location in the scene, such as the surface of the table. \n"
    prompt += "19.Position {object1} at equal distance from {object2} and {object3}. Where object1, object2 and object3 are specific objects in the scene. \n"
    prompt += "20.Stack {object1, object2, ...}. Where object1 and object2 are specific objects in the scene. \n"
    prompt += "21.Count the number of {object}. Where object is a type of object in the scene. \n"
    prompt += "22.Which {object} is biggest/smallest/farthest/nearest? Where object is a type of object in the scene. \n"
    prompt += "23.Which room has the most {object}? Where object is a type of object in the scene. \n"
    prompt += "24.Compare the sizes of {object1} and {object2}. Where object1 and object2 are specific objects in the scene. \n"
    prompt += "If there are multiple objects of the same type or similar types in the scene, then when constructing the task, you need to clearly and unambiguously state which vase the object in the task refers to. This can be referred to by the characteristics of the object itself, such as color, shape, or by its spatial position in the scene.  If there are three vases in a scene, then the task at this time can be structured as: go to {the vase on the edge of the table}, or: go to {the green round vase}. \n"
    prompt += "Please combine scene and object information to generate a series of tasks based on the task template, for example: go to the chair farthest from me, count the number of the yellow vases. \n"
    prompt += "Please generate 3-4 tasks according to each template. The tasks must comply with common sense and rules to avoid tasks such as pick up the bed. \n"
    prompt += "Note that as a robot assistant, you only have visual abilities and no tactile, hearing or other abilities. Therefore, you can only see the color, size, shape and other information of the cushions, but cannot judge whether the cushions are soft or new or old. \n"
    prompt += "After you generate a task, use diverse language but be precise in your description. For example: Tell me the number of the green vases; Please go to the green cushion. \n"
    prompt += "Please follow the following format for your answer: \n"
    prompt += "TASK:go to the red cushion. \n"
    prompt += "TASK:tell me the number of the cups on the table. \n"

    print("\n\n" + prompt + "\n\n")

    return get_response_new(prompt)
