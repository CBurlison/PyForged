import sys
sys.path.append("...")

import pygame
from ForgedTypes.node import Node

class MainMenu(Node):
    def __init__(self):
        super().__init__()
        self.first: bool = True

    def process(self, delta: float):
        # Draw a solid blue circle in the center
        #pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

        surf = pygame.Surface((50, 50))
        surf.fill((0, 0, 0))
        
        self.screen.blit(surf, (250, 250))

        if self.first:
            surf2 = pygame.Surface((10, 10))
            surf2.fill((255, 255, 255))
            
            self.screen.blit(surf2, (260, 260))
            self.first = False
        else:
            self.first = True
