import pygame

class ImageStore:
    def __init__(self):
        self.images: dict[str, pygame.Surface] = {}

        self.images["TestAtlas"] = pygame.image.load("./Assets/Sprites/TestAtlas.png").convert_alpha()

    def get_image(self, image_name: str) -> pygame.surface:
        return self.images[image_name]