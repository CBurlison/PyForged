from typing_extensions import Self
from enum import Enum
import pygame

class MouseInterraction(Enum):
    Stop = 0
    Ignore = 1

class Node:
    def __init__(self):
        # init sets up new variables and does DI stuff. Always call super().__init__().
        self.__new_node: bool = True
        self.__visible: bool = True
        self.__process: bool = True

        self.on_enter_tree: list[any] = None
        self.on_exit_tree: list[any] = None

        self.parent: Self = None
        self.children: list[Self] = []
        self.mouse_interaction: MouseInterraction = MouseInterraction.Stop

        self.surface: pygame.Surface = None
        self.surface_rect: pygame.Rect = None
        self.size: tuple[int, int] = (0, 0)
        self.position: tuple[int, int] = (0, 0)
        self.color: tuple[int, int, int] = (0, 0, 0)
        
        # set in DI
        self.game_tree: Self = None
        self.screen: pygame.Surface = None

    def setup(self):
        # called in DI after setting things like screen and game_tree.
        pass

    def process(self, delta: float):
        # called every frame. delta is last frame time in seconds
        pass

    def enter_tree(self):
        # called when first entering tree with add_child
        pass

    def exit_tree(self):
        # called when finally exiting tree with free()
        pass

    def add_child(self, new_child: Self):
        # adds a child to this node and calls enter tree events if first time added
        if new_child.parent is not None:
            new_child.parent.remove_child(new_child)

        new_child.parent = self
        self.children.append(new_child)

        if new_child.__new_node:
            new_child.__new_node = False
            new_child.enter_tree()
            new_child.game_tree.__enter_tree_events(self)

    def remove_child(self, to_remove: Self):
        # removes child from this node
        to_remove.parent = None

        if to_remove in self.children:
            _ = self.children.pop(to_remove)

    def reparent(self, new_parent: Self):
        # changes the parent of this node to another node
        if self.parent is None:
            raise ValueError("Node must have a parent in order to reparent.")
            
        self.parent.remove_child(self)
        new_parent.add_child(self)

    def free(self):
        # removes this node from its parent and the tree. calls exit tree events
        if self.parent is not None:
            self.parent.remove_child(self)
            
        self.exit_tree()
        self.game_tree.__exit_tree_events(self)

        for child in self.children:
            child.free()

    def set_visible(self, visible: bool = True):
        self.__visible = visible

    def is_visible(self) -> bool:
        if not self.__visible:
            return False
        
        if self.parent is not None:
            return self.parent.is_visible()

        return True

    def set_process(self, process: bool = True):
        self.__process = process

    def move(self, amount: tuple[int, int]):
        if self.surface_rect is not None:
            self.surface_rect.x += amount[0]
            self.surface_rect.y += amount[1]
            self.position = (self.surface_rect.x, self.surface_rect.y)
        else:
            self.position = (self.position[0] + amount[0], self.position[1] + amount[1])
            
        self.__move_children(amount)

    def update_surface(self):
        self.surface = pygame.Surface(self.size)
        self.surface.fill(self.color)

        self.surface_rect = self.surface.get_rect()
        self.surface_rect.x += self.position[0]
        self.surface_rect.y += self.position[1]
        
    def __move_children(self, amount: tuple[int, int]):
        for child in self.children:
            if child.surface_rect is not None:
                child.surface_rect.x += amount[0]
                child.surface_rect.y += amount[1]
                child.position = (child.surface_rect.x, child.surface_rect.y)
            else:
                child.position = (child.position[0] + amount[0], child.position[1] + amount[1])
                
            child.__move_children(amount)
        
    def __move_children_to(self, position: tuple[int, int]):
        for child in self.children:
            if child.surface_rect is not None:
                child.surface_rect.move(position)
                child.position = (child.surface_rect.x, child.surface_rect.y)
            else:
                child.position = position

            child.__move_children_to(position)

    def __draw(self):
        if self.surface is not None and self.screen is not None:
            self.screen.blit(self.surface, self.position)

        self.__draw_children(self)
        
    def __draw_children(self, process_node: Self):
        for child in process_node.children:
            if child.__visible:
                child.__draw()
                self.__draw_children(child)
            
    # tree methods
    def __process_children(self, process_node: Self, delta: float):
        pass

    def __enter_tree_events(self, new_node: Self):
        pass

    def __exit_tree_events(self, removed_node: Self):
        pass
