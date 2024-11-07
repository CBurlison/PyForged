import sys
sys.path.append("...")

from ForgedTypes.control import Control

class FlashyBox(Control):
    def __init__(self):
        super().__init__()
        self.flash: bool = True
        self.timer: float = 0.0
        
        self.color = (255, 255, 255)
        self.flash_time: float = 2.0

    def setup(self):
        self.update_surface()

    def process(self, delta: float):
        self.timer += delta

        if self.timer >= self.flash_time:
            self.timer -= self.flash_time

            self.flash = not self.flash
            self.set_visible(self.flash)
            
