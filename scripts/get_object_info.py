import re


# 获取场景中的所有物体信息
def get_scene_object_info(scene):
    instances = scene["instances"]
    object_info = {}
    for dic in instances:
        object_name = re.findall(
            r"[A-Za-z]+", dic["prefab"].split("_")[1]
        )  # 提取出物体名称
        object_name = " ".join(object_name)
        # TODO 如果多房间可能涉及door
        if object_name != "Floor" and object_name != "Wall":  # 不统计地板和墙
            object_info[object_name] = object_info.get(object_name, 0) + 1
    return object_info  # dic{object_name:object_num}


# 获取agent第一视角画面中的物体信息
def get_ego_object_list(visible_objects):
    object_info = {}
    for obj in visible_objects:
        object_name = re.findall(r"[A-Za-z]+", obj.split("_")[1])
        object_name = " ".join(object_name)
        if object_name != "Floor" and object_name != "Wall":
            object_info[object_name] = object_info.get(object_name, 0) + 1
    return object_info  # dic{object_name:object_num}
