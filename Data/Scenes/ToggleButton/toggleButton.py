from Data.Models.transform import Transform, SizeMode
from Data.Nodes.Controls.Sprites.button import Button
from Data.GameData.imageStore import ImageStore

class ToggleButton(Button):
    def __init__(self, transform: Transform, image_store: ImageStore):
        super().__init__("Button", transform, image_store)
        self.name = "ToggleButton"

    def setup(self):
        super().setup()
        
        self.clicked_img = "ButtonPressed"
        self.hovered_img = "ButtonHovered"
        self.toggled_img = "ButtonSelected"
        self.toggled_hovered_img = "ButtonSelectedHovered"
        self.transform.size_mode = SizeMode.Sprite
        self.unique_toggle = True
        self.toggable = True