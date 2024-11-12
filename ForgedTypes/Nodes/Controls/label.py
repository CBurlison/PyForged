import sys
sys.path.append("....")

import pygame.font as font
from ForgedTypes.Nodes.Controls.control import Control
from Assets.Fonts.fontInfo import FontInfo

class Label(Control):
    def __init__(self, new_font: FontInfo, text: str):
        super().__init__()
        self.__font_info = new_font
        self.font = font.SysFont(new_font.font, new_font.size, new_font.bold, new_font.italic)

        self.text = text

    @property
    def font_info(self) -> FontInfo:
        return self.__font_info
    
    @font_info.setter
    def font_info(self, new_font: FontInfo):
        self.__font_info = new_font
        self.font = font.SysFont(new_font.font, new_font.size, new_font.bold, new_font.italic)

    def update_surface(self):
        self.surface = self.font.render(self.text, False, self.font_info.color)
        
        self.set_rect()
