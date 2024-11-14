import sys
sys.path.append("....")

import pygame
from Data.GameData.imageStore import ImageStore
from Data.ForgedTypes.Nodes.Controls.control import Control
from Data.ForgedTypes.Models.transform import Transform, SizeMode

class Sprite(Control):
    def __init__(self, transform: Transform, image_store: ImageStore):
        super().__init__()
        self.image_store = image_store

        self.transform = transform
        self.transform.owner = self
        self.__sprite: str = ""

    @property
    def sprite(self) -> str:
        return self.__sprite
        
    @sprite.setter
    def sprite(self, new_sprite: str):
        if self.__sprite == new_sprite:
            return

        self.__sprite = new_sprite
        self.surface = self.image_store.get_image(new_sprite)
        self.update_surface(True)

    def update_surface(self, force: bool = False):
        if self.surface is None:
            self.surface = pygame.Surface((1, 1))

        self.set_rect()

        scale_w = self.transform.scale
        scale_h = self.transform.scale

        if self.transform.size_mode == SizeMode.Size:
            if self.rect.w > 0 and self.transform.size[0] > 0:
                scale_w *= (self.transform.size[0] / self.rect.w)
            if self.rect.h > 0 and self.transform.size[1] > 0:
                scale_h *= (self.transform.size[1] / self.rect.h)

        if scale_w != 1.0 or scale_h != 1.0:
            self.surface = pygame.transform.scale(self.surface, (self.rect.w * scale_w, self.rect.h * scale_h))
            self.set_rect()
        
        self.surface.set_colorkey(self.color)