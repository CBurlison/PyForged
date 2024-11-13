import sys
sys.path.append("....")

import pygame
from Data.ForgedTypes.Nodes.Controls.control import Control
from Data.ForgedTypes.Models.fontInfo import FontInfo

true_black: tuple[int, int, int] = (0, 0, 0)

class Label(Control):
    def __init__(self, new_font: FontInfo, text: str):
        super().__init__()
        self.__text: str = ""

        self.font_info: FontInfo = new_font
        self.text: str = text

    @property
    def text(self):
        return self.__text

    @text.setter
    def text(self, new_text: str):
        if new_text == self.__text:
            return

        self.__text = new_text
        self.update_surface()

    @property
    def font_info(self) -> FontInfo:
        return self.__font_info
    
    @font_info.setter
    def font_info(self, new_font: FontInfo):
        self.__font_info = new_font
        self.font = pygame.font.SysFont(new_font.font, new_font.size, new_font.bold, new_font.italic)

        if self.text != "":
            self.update_surface()

    def update_surface(self):
        if self.font_info.outline > 0:
            self.surface = self.text_outline(self.font, self.text, self.font_info.color, self.font_info.outline_color)
        else:
            self.surface = self.font.render(self.text, 0, self.font_info.color)

        self.set_rect()

    def text_hollow(self, font: pygame.font.Font, message: str, fontcolor):
        notcolor = [c^0xFF for c in fontcolor]
        base = font.render(message, 0, fontcolor)
        size = base.get_width() + self.font_info.outline*2, base.get_height() + self.font_info.outline*2
        img = pygame.Surface(size, 16)
        img.fill(notcolor)
        img.set_colorkey(true_black)
        img.blit(base, (0, 0))
        img.blit(base, (self.font_info.outline, 0))
        img.blit(base, (0, self.font_info.outline))
        img.blit(base, (self.font_info.outline, self.font_info.outline))
        img.set_colorkey(true_black)
        base.set_palette_at(1, notcolor)
        img.blit(base, (self.font_info.outline, self.font_info.outline))
        img.set_colorkey(notcolor)
        return img

    def text_outline(self, font: pygame.font.Font, message: str, fontcolor, outlinecolor):
        base = font.render(message, 0, fontcolor)
        outline = self.text_hollow(font, message, outlinecolor)
        size = base.get_width() + self.font_info.outline*2, base.get_height() + self.font_info.outline*2
        img = pygame.Surface(size, 16)
        img.blit(outline, (0, 0))
        img.blit(base, (self.font_info.outline, self.font_info.outline))
        img.set_colorkey(true_black)
        return img