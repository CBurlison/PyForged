import sys
sys.path.append("...")

import pygame
from ForgedTypes.control import Control
from PythonDI import DIContainer

class FlashyBox(Control):
    def __init__(self, container: DIContainer):
        super().__init__()
        self.flash: bool = True
        self.container: DIContainer = container
        self.timer: float = 0.0
        
        self.color: tuple[int, int, int] = (255, 255, 255)
        self.flash_time: float = 2.0

    def process(self, delta: float):
        self.timer += delta

        if self.flash:
            surf2 = pygame.Surface(self.size)
            surf2.fill(self.color)
            
            self.screen.blit(surf2, self.position)

        if self.timer >= self.flash_time:
            self.timer -= self.flash_time

            self.flash = not self.flash
