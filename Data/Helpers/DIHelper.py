import Data.Scenes.MainMenu.mainMenu as mainMenu
import Data.Scenes.FpsCounter.fpsCounter as fpsCounter
import Data.Scenes.ToggleButton.toggleButton as toggleButton
import Data.Nodes.Controls.label as label
from Data.PythonDI import DIContainer
from Data.sceneManager import SceneManager
from Data.Factories.nodeFactory import NodeFactory
from Data.Models.gameState import GameState
from Data.Models.transform import Transform
from Data.Nodes.Controls.Sprites.sprite import Sprite
from Data.Nodes.Controls.Sprites.animatedSprite import AnimatedSprite
from Data.Nodes.Controls.Sprites.button import Button
from Data.GameData.animationStore import AnimationStore
from Data.GameData.imageStore import ImageStore

def register_nodes(di_container: DIContainer):
    di_container.register_instance(NodeFactory)
    di_container.register_instance(GameState)
    di_container.register_instance(AnimationStore)
    di_container.register_instance(SceneManager)

    di_container.register(mainMenu.MainMenu)
    di_container.register(label.Label)
    di_container.register(fpsCounter.FpsCounter)
    di_container.register(AnimatedSprite)
    di_container.register(Sprite)
    di_container.register(ImageStore)
    di_container.register(Transform)
    di_container.register(Button)
    di_container.register(toggleButton.ToggleButton)
