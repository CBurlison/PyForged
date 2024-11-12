import sys
sys.path.append(".")

import pygame
from Helpers import ImageHelper


class ImageStore:
    def __init__(self):
        self.images: dict[str, pygame.Surface] = {}

        self.images["TestAtlas"] = pygame.image.load("./Assets/Sprites/TestAtlas.png").convert_alpha()

        self.images["Human_Portrait"] = ImageHelper.create_atlas_surface(self.images["TestAtlas"], (1048, 2088), 512, 512)

    def get_image(self, image_name: str) -> pygame.surface:
        return self.images[image_name]