from enum import Enum

class SizeMode(Enum):
    Size = 0
    Sprite = 1

class Transform:
    def __init__(self):
        self.__position: tuple[int, int] = (0, 0)
        self.size: tuple[int, int] = (0, 0)
        self.size_mode: SizeMode = SizeMode.Size
        self.scale: float = 1.0
        self.owner = None

    @property
    def position(self):
        return self.__position
    
    @position.setter
    def position(self, new_pos: tuple[int, int]):
        self.__position = new_pos

        if self.owner is not None and self.owner.surface is not None:
            self.owner.set_rect()
        