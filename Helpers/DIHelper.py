import sys
sys.path.append("..")

from PythonDI import *
from Scenes.MainMenu.MainMenu import MainMenu

def register_nodes(di_container: DIContainer):
    di_container.register(MainMenu)
