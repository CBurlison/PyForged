import sys
sys.path.append("..")

import Scenes.MainMenu.mainMenu as mainMenu
import Scenes.FpsCounter.fpsCounter as fpsCounter
import Scenes.MainMenu.flashyBox as flashyBox
import ForgedTypes.Nodes.Controls.label as label
from PythonDI import DIContainer
from ForgedTypes.Models.transform import Transform
from ForgedTypes.Nodes.Controls.Sprites.sprite import Sprite
from ForgedTypes.Nodes.Controls.Sprites.animatedSprite import AnimatedSprite
from Data.animationStore import AnimationStore
from Data.imageStore import ImageStore

def register_nodes(di_container: DIContainer):
    di_container.register(mainMenu.MainMenu)
    di_container.register(flashyBox.FlashyBox)
    di_container.register(label.Label)
    di_container.register(fpsCounter.FpsCounter)
    di_container.register(AnimatedSprite)
    di_container.register(Sprite)
    di_container.register(AnimationStore)
    di_container.register(ImageStore)
    di_container.register(Transform)
