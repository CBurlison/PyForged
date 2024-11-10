import sys
sys.path.append("...")
sys.path.append("....")

import pygame
from ForgedTypes.Nodes.Controls.label import Label
from Assets.Fonts.fontInfo import FontInfo

class FpsCounter(Label):
    def __init__(self, clock: pygame.time.Clock):
        super().__init__(FontInfo(size=36, color=(218, 165, 32), bold=True), "0")
        self.clock = clock

    def process(self, delta: float):
        super().process(delta)

        self.text = f"{self.clock.get_fps():.2f}"
        self.update_surface()
