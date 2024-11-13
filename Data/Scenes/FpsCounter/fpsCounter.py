import sys
sys.path.append("....")

import pygame
from Data.ForgedTypes.Nodes.Controls.label import Label
from Data.ForgedTypes.Models.fontInfo import FontInfo

class FpsCounter(Label):
    def __init__(self, clock: pygame.time.Clock):
        self.clock = clock
        super().__init__(FontInfo(size=36, color=(218, 165, 32), bold=True, outline=3), f"{clock.get_fps():.2f}")

    def process(self, delta: float):
        super().process(delta)

        self.text = f"{self.clock.get_fps():.2f}"
