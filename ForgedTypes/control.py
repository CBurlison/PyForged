import sys
sys.path.append("...")

from ForgedTypes.node import Node

class Control(Node):

    def __init__(self):
        super().__init__()
        self.flash: bool = True
        
        self.size: tuple[int, int] = (0, 0)
        self.position: tuple[int, int] = (0, 0)
