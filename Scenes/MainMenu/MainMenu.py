import sys
sys.path.append("...")

import pygame
from ForgedTypes.node import Node
from ForgedTypes.tree import Tree

class MainMenu(Node):
    first: bool = True

    def __init__(self, game_tree: Tree):
        self.game_tree = game_tree
        super().__init__()

    def process(self, delta: float):
        # Draw a solid blue circle in the center
        #pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

        surf = pygame.Surface((50, 50))
        surf.fill((0, 0, 0))
        
        self.game_tree.screen.blit(surf, (250, 250))

        if self.first:
            surf2 = pygame.Surface((10, 10))
            surf2.fill((255, 255, 255))
            
            self.game_tree.screen.blit(surf2, (260, 260))
            self.first = False
        else:
            self.first = True
