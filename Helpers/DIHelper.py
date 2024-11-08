import sys
sys.path.append("..")

import Scenes.MainMenu.mainMenu as mainMenu
import Scenes.MainMenu.flashyBox as flashyBox
import ForgedTypes.Nodes.Controls.label as label
from PythonDI import DIContainer

def register_nodes(di_container: DIContainer):
    di_container.register(mainMenu.MainMenu)
    di_container.register(flashyBox.FlashyBox)
    di_container.register(label.Label)
