from enum import Enum

class SizeMode(Enum):
    Size = 0
    Sprite = 1

class Transform:
    def __init__(self):
        self.position: tuple[int, int] = (0, 0)
        self.size: tuple[int, int] = (0, 0)
        self.size_mode: SizeMode = SizeMode.Size
        self.scale: float = 1.0