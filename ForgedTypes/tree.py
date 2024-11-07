from ForgedTypes.node import Node
import pygame

class Tree(Node):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self.children: list[Node] = []
        self.screen = screen
        self.game_tree = self

    def process(self, delta: float):
        self.__process_children(self, delta)

    def draw(self):
        self.__draw()
        
    def __process_children(self, process_node: Node, delta: float):
        for child in process_node.children:
            if child._Node__process:
                child.process(delta)

            self.__process_children(child, delta)
            
    def __draw(self):
        for child in self.children:
            if child._Node__visible:
                child._Node__draw()
            
    def __enter_tree_events(self, new_node: Node):
        for ev in self.on_enter_tree:
            ev(new_node)

    def __exit_tree_events(self, removed_node: Node):
        for ev in self.on_exit_tree:
            ev(removed_node)
