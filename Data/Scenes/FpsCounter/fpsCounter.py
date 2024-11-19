import pygame
from Data.Nodes.Controls.label import Label
from Data.Nodes.Controls.control import AnchorPoint
from Data.Models.fontInfo import FontInfo

class FpsCounter(Label):
    def __init__(self, clock: pygame.time.Clock):
        self.clock = clock
        super().__init__(FontInfo(size=36, color=(218, 165, 32), bold=True, outline=3), f"{clock.get_fps():.2f}")

    def setup(self):
        super().setup()
        self.transform.position = (0, 60)
        self.transform.size = (1920, 60)
        self.anchor_point = AnchorPoint.TopCenter
    
    def process(self, delta: float):
        super().process(delta)

        self.text = f"{self.clock.get_fps():.2f}"
