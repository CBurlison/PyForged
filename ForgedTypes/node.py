from typing_extensions import Self
from enum import Enum
import pygame

class MouseInterraction(Enum):
    Stop = 0
    Ignore = 1

class Node:
    def __init__(self):
        self.parent: Self = None
        self.children: list[Self] = []
        self.mouse_interaction: MouseInterraction = MouseInterraction.Stop
        self.game_tree: Self = None
        self.screen: pygame.Surface = None

    def setup(self):
        pass

    def process(self, delta: float):
        pass

    def add_child(self, new_child: Self):
        if new_child.parent is not None:
            new_child.parent.remove_child(new_child)
            
        new_child.parent = self
        self.children.append(new_child)

    def remove_child(self, to_remove: Self):
        if to_remove in self.children:
            _ = self.children.pop(to_remove)
            to_remove.parent = None

    def reparent(self, new_parent: Self):
        if self.parent is not None:
            self.parent.remove_child(self)

        new_parent.add_child(self)
            
    def __process_children(self, process_node: Self, delta: float):
        pass