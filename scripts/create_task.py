from legent import (
    Environment,
    ResetInfo,
    generate_scene,
    TakePhotoWithVisiblityInfo,
    store_json,
)
import os
from scripts.gpt_api import get_response_new, get_response_4v


save_folder = f"{os.getcwd()}/test_dataset"  # 测试数据集路径
os.makedirs(save_folder, exist_ok=True)

env = Environment(env_path="auto")

scene_num = 1  # 生成场景数量

try:
    for i in range(scene_num):
        absolute_path = f"{save_folder}/{scene_num:04d}"  # 当前文件夹路径
        os.makedirs(absolute_path, exist_ok=True)

        scene = generate_scene(room_num=1)
        print(f"\n\nscene {i} generated\n\n")

        position = scene["agent"]["position"].copy()  # 位置
        position[1] += 1

        rotation = scene["agent"]["rotation"]  # 角度

        photo_path = f"{absolute_path}/photo.png"  # 图片路径
        obs = env.reset(
            ResetInfo(
                scene,
                api_calls=[
                    TakePhotoWithVisiblityInfo(
                        photo_path,
                        position,
                        rotation,
                        width=4096,
                        height=4096,
                        vertical_field_of_view=90,
                        rendering_type="",
                    )
                ],
            )
        )

        visible_objects = [
            scene["instances"][object_id]["prefab"]
            for object_id in obs.api_returns["objects_in_view"]
        ]
        print("api_returns:\n", obs.api_returns)
        print("visible_objects:\n", visible_objects)

        store_json(visible_objects, f"{absolute_path}/visible_objects.json")
finally:
    env.close()
