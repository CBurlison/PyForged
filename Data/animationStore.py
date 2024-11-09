import sys
sys.path.append(".")

from Data.imageStore import ImageStore
from ForgedTypes.Animation.animation import Animation
from Helpers import AnimationHelper

class AnimationStore:
    def __init__(self, image_store: ImageStore):
        self.animations: dict[str, Animation] = {}

        anim = Animation([
            AnimationHelper.create_atlas_frame(image_store.images["TestAtlas"], (8, 3128), 512, 512),
            AnimationHelper.create_atlas_frame(image_store.images["TestAtlas"], (528, 3128), 512, 512),
            AnimationHelper.create_atlas_frame(image_store.images["TestAtlas"], (1048, 3128), 512, 512),
            AnimationHelper.create_atlas_frame(image_store.images["TestAtlas"], (1568, 3128), 512, 512)
        ], 6, True)
        self.animations["Human_Idle"] = anim