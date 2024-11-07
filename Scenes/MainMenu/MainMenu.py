import sys
sys.path.append("...")

import pygame
from ForgedTypes.control import Control
from PythonDI import DIContainer
from Scenes.MainMenu.flashy_box import FlashyBox

class MainMenu(Control):
    def __init__(self, container: DIContainer):
        super().__init__()
        self.container: DIContainer = container

    def setup(self):
        self.position = (250, 250)
        self.size = (50, 50)

        box: FlashyBox = self.container.locate(FlashyBox)
        box.size = (10, 10)
        box.position = (260, 260)

        self.add_child(box)

    def process(self, delta: float):
        surf = pygame.Surface(self.size)
        surf.fill((0, 0, 0))
        
        self.screen.blit(surf, self.position)
