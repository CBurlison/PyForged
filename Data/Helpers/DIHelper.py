import sys
sys.path.append("...")

import Data.Scenes.MainMenu.mainMenu as mainMenu
import Data.Scenes.FpsCounter.fpsCounter as fpsCounter
import Data.Scenes.MainMenu.flashyBox as flashyBox
import Data.ForgedTypes.Nodes.Controls.label as label
from Data.PythonDI import DIContainer
from Data.ForgedTypes.Models.transform import Transform
from Data.ForgedTypes.Nodes.Controls.Sprites.sprite import Sprite
from Data.ForgedTypes.Nodes.Controls.Sprites.animatedSprite import AnimatedSprite
from Data.ForgedTypes.Nodes.Controls.Sprites.button import Button
from Data.GameData.animationStore import AnimationStore
from Data.GameData.imageStore import ImageStore

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
    di_container.register(Button)
