import sys

import Scenes.MainMenu
import Scenes.MainMenu.MainMenu
import Scenes.MainMenu.flashy_box
sys.path.append("..")

from PythonDI import DIContainer
import Scenes

def register_nodes(di_container: DIContainer):
    di_container.register(Scenes.MainMenu.MainMenu.MainMenu)
    di_container.register(Scenes.MainMenu.flashy_box.FlashyBox)
