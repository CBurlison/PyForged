from ForgedTypes.node import Node
import pygame

class Tree(Node):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self.screen = screen
        self.game_tree = self

    def process(self, delta: float):
        self.__process_children(self, delta)
        
    def __process_children(self, process_node: Node, delta: float):
        for child in process_node.children:
            child.process(delta)
            self.__process_children(child, delta)
            