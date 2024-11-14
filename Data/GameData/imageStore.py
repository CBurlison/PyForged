import pygame
from Data.Helpers import ImageHelper

class ImageStore:
    def __init__(self):
        self.images: dict[str, pygame.Surface] = {}

        self.images["TestAtlas"] = pygame.image.load("./Data/Assets/Sprites/TestAtlas.png").convert_alpha()
        self.images["Button"] = pygame.image.load("./Data/Assets/Sprites/buttonLong_brown.png").convert_alpha()
        self.images["ButtonPressed"] = pygame.image.load("./Data/Assets/Sprites/buttonLong_brown_pressed.png").convert_alpha()
        self.images["ButtonHovered"] = pygame.image.load("./Data/Assets/Sprites/buttonLong_brown_hovered.png").convert_alpha()
        self.images["ButtonSelected"] = pygame.image.load("./Data/Assets/Sprites/buttonLong_brown_selected.png").convert_alpha()
        self.images["ButtonSelectedHovered"] = pygame.image.load("./Data/Assets/Sprites/buttonLong_brown_selected_hovered.png").convert_alpha()

        self.images["Human_Portrait"] = ImageHelper.create_atlas_surface(self.images["TestAtlas"], (1048, 2088), 512, 512)

    def get_image(self, image_name: str) -> pygame.surface:
        return self.images[image_name]