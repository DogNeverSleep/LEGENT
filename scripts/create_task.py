from legent import (
    Environment,
    ResetInfo,
    generate_scene,
    TakePhotoWithVisiblityInfo,
    store_json,
)
import os
import json
from scripts.gpt_api import get_response_new, get_response_4v
from scripts.get_object_info import (
    get_scene_object_info,
    get_ego_object_list,
    get_scene_object_info_new,
)
from scripts.prompt_create_task import (
    scene_to_description,
    description_to_task,
    description_to_task_QA,
    description_to_task_action,
)
import pandas as pd


# save_folder = f"{os.getcwd()}/test_dataset"  # 测试数据集路径
save_folder = "/data41/private/legent/LEGENT/test_dataset"  # 测试数据集路径
os.makedirs(save_folder, exist_ok=True)

env = Environment(env_path="auto")

scene_num = 1  # 生成场景数量

try:
    for i in range(scene_num, scene_num + 1):
        absolute_path = f"{save_folder}/{i:04d}"  # 当前场景的文件夹路径
        os.makedirs(absolute_path, exist_ok=True)

        # legent生成场景
        # scene = generate_scene(room_num=1)
        # print(f"\n\nscene {i} generated\n\n")

        # 载入事先构造好的场景
        scene_json = "scene_data/test_scenes_2/two_rooms/20240529-224622-154114.json"
        with open(scene_json, "r", encoding="utf-8") as file:
            scene = json.load(file)
        print(f"\n\nscene {i} loaded\n\n")

        position = scene["agent"]["position"].copy()  # 位置
        # position = scene["player"]["position"].copy()
        # position[1] += 1

        # 从agent的四个方向拍照
        for j in range(4):
            rotation = scene["player"]["rotation"].copy()  # 角度
            rotation[1] = (rotation[1] + j * 90) % 360
            # print("rotation:", rotation)

            photo_path = f"{absolute_path}/photo_{j}.png"  # 图片路径

            obs = env.reset(
                ResetInfo(
                    scene,
                    api_calls=[
                        TakePhotoWithVisiblityInfo(
                            photo_path,
                            position,
                            rotation,
                            width=1024,
                            height=int(1024 * 90 / 120),
                            vertical_field_of_view=90,
                            rendering_type="",
                        )
                    ],
                )
            )

            # if j == 0:  # agent第一视角
            #     visible_objects = [
            #         scene["instances"][object_id]["prefab"]
            #         for object_id in obs.api_returns["objects_in_view"]
            #     ]
            #     ego_object_info = get_ego_object_list(
            #         visible_objects
            #     )  # agent第一视角画面中的物体信息 dic{object_name:object_num}
            #     store_json(ego_object_info, f"{absolute_path}/ego_object_info.json")

        object_info, room_object_info = get_scene_object_info_new(
            scene
        )  # 场景中的所有物体信息 dic{index:category}
        store_json(object_info, f"{absolute_path}/scene_object_info.json")
        store_json(room_object_info, f"{absolute_path}/room_object_info.json")

        print("\n\nstart to generate scene description\n\n")
        scene_description = scene_to_description(
            absolute_path, object_info, room_object_info
        )  # 场景描述
        print("\n\n" + scene_description + "\n\n")

        print("\n\nstart to generate task\n\n")
        tasks = description_to_task_QA(
            scene_description, object_info, room_object_info
        )  # 生成QA类任务
        # tasks = description_to_task_action(scene_description, object_info, room_object_info)  # 生成执行类任务
        print("\n\n" + tasks + "\n\n")
        store_json(tasks, f"{absolute_path}/task.json")

        store_json(scene, f"{absolute_path}/scene.json")

        print(f"\n\nscene {i} finished\n\n")
finally:
    env.close()
