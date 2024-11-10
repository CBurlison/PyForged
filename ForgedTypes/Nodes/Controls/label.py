import sys
sys.path.append("....")

import pygame.font as font
from ForgedTypes.Nodes.Controls.control import Control
from Assets.Fonts.fontInfo import FontInfo

class Label(Control):
    def __init__(self, font_info: FontInfo, text: str):
        super().__init__()
        self.font_info = font_info
        self.text = text

    def update_surface(self):
        new_font = font.SysFont(self.font_info.font, self.font_info.size, self.font_info.bold, self.font_info.italic)
        self.surface = new_font.render(self.text, False, self.font_info.color)
        
        self.rect = self.surface.get_rect()
        self.rect.x += self.position[0]
        self.rect.y += self.position[1]
