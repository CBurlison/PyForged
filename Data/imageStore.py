import pygame

class ImageStore:
    def __init__(self):
        self.images: dict[str, pygame.Surface] = {}

        self.images["TestAtlas"] = pygame.image.load("./Assets/Sprites/TestAtlas.png").convert_alpha()