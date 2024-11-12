import sys
sys.path.append(".")

from Data.imageStore import ImageStore
from ForgedTypes.Animation.animation import Animation
from Helpers import ImageHelper

class AnimationStore:
    def __init__(self, image_store: ImageStore):
        self.animations: dict[str, Animation] = {}

        anim = Animation([
            ImageHelper.create_atlas_animation_frame(image_store.get_image("TestAtlas"), (8, 3128), 512, 512),
            ImageHelper.create_atlas_animation_frame(image_store.get_image("TestAtlas"), (528, 3128), 512, 512),
            ImageHelper.create_atlas_animation_frame(image_store.get_image("TestAtlas"), (1048, 3128), 512, 512),
            ImageHelper.create_atlas_animation_frame(image_store.get_image("TestAtlas"), (1568, 3128), 512, 512)
        ], 6, True)
        self.animations["Human_Idle"] = anim

    def get_animation(self, anim_name: str) -> Animation:
        return self.animations[anim_name]