import re
import pandas as pd


# 读取原始物体的名称-类别
def get_object_category(csv_file="/Users/frank/Code/LEGENT/test_dataset/assets.csv"):
    df = pd.read_csv(csv_file)
    prefab_column = df.iloc[:, 0]
    category_column = df.iloc[:, 2]
    # print(first_column)
    object_category = {}
    for i in range(len(prefab_column)):
        if not pd.isna(category_column[i]):
            name = prefab_column[i].split("/")[-1]
            name = name.split(".")[0]
            object_category[name] = category_column[i]
    return object_category  # {name:category}


# 获取场景中的所有物体信息
def get_scene_object_info(scene):
    object_category = get_object_category()
    instances = scene["instances"]
    object_info = {}
    index = 0  # 物体索引 scene["instances"]中第index个物体
    for dic in instances:
        object_name = re.findall(
            r"[A-Za-z]+", dic["prefab"].split("_")[1]
        )  # 提取出物体名称
        object_name = " ".join(object_name)
        # TODO 如果多房间可能涉及door
        if object_name != "Floor" and object_name != "Wall":  # 不统计地板和墙
            # object_info[object_name] = object_info.get(object_name, 0) + 1
            object_name = dic["prefab"].split("_")[1:]
            object_name = "_".join(object_name)
            if object_name in object_category:
                object_info[index] = object_category[object_name]
            else:
                object_info[index] = object_name
        index += 1
    return object_info  # dic{index:object_name}


# 新版场景下获取所有物体信息
def get_scene_object_info_new(scene):
    pass


# 获取agent第一视角画面中的物体信息
def get_ego_object_list(visible_objects):
    object_info = {}
    for obj in visible_objects:
        object_name = re.findall(r"[A-Za-z]+", obj.split("_")[1])
        object_name = " ".join(object_name)
        if object_name != "Floor" and object_name != "Wall":
            object_info[object_name] = object_info.get(object_name, 0) + 1
    return object_info  # dic{object_name:object_num}
