import sys
sys.path.append("...")

from ForgedTypes.Animation.animationFrame import AnimationFrame

class Animation:
    def __init__(self, frames: list[AnimationFrame] = [], fps: int = 12, loop: bool = False) -> None:
        self.frames: list[AnimationFrame] = frames
        self.fps: int = fps
        self.loop: bool = loop
