import sys
sys.path.append(".")

from pygame import Surface
from ForgedTypes.node import Node

class Tree(Node):
    def __init__(self, screen: Surface):
        self.screen = screen
        super().__init__()

    def process(self, delta: float):
        self.__process_children(self, delta)
        
    def __process_children(self, process_node: Node, delta: float):
        for child in process_node.children:
            child.process(delta)
            self.__process_children(child, delta)