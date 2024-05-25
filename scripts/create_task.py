from legent import (
    Environment,
    ResetInfo,
    generate_scene,
    TakePhotoWithVisiblityInfo,
    store_json,
)
import os
from scripts.gpt_api import get_response_new, get_response_4v


save_folder = f"{os.getcwd()}/photo_views"
os.makedirs(save_folder, exist_ok=True)
env = Environment(env_path="auto")

try:
    for i in range(10):
        absolute_path = f"{save_folder}/{i:04d}.png"
        print(f"save photo of scene {i} to {absolute_path}")
        scene = generate_scene(room_num=1)
        position = scene["agent"]["position"].copy()
        position[1] += 1
        rotation = scene["agent"]["rotation"]
        obs = env.reset(
            ResetInfo(
                scene,
                api_calls=[
                    TakePhotoWithVisiblityInfo(
                        absolute_path,
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
        print(obs.api_returns)
        print(visible_objects)
        store_json(visible_objects, f"{save_folder}/{i:04d}.json")

        # save segmentation image
        absolute_path = f"{save_folder}/{i:04d}.seg.png"
        obs = env.reset(
            ResetInfo(
                scene,
                api_calls=[
                    TakePhotoWithVisiblityInfo(
                        absolute_path,
                        position,
                        rotation,
                        width=4096,
                        height=4096,
                        vertical_field_of_view=90,
                        rendering_type="segmentation",
                    )
                ],
            )
        )
finally:
    env.close()
