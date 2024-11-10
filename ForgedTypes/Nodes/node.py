import pygame
from ForgedTypes.gameState import GameState

class Node:
    def __init__(self):
        # init sets up new variables and does DI stuff. Always call super().__init__().
        self.__new_node: bool = True
        self.visible: bool = True
        self.run_process: bool = True
        
        self.parent: "Node" = None
        self.children: list["Node"] = []

        self.surface: pygame.Surface = None
        self.rect: pygame.Rect = None
        self.size: tuple[int, int] = (0, 0)
        self.position: tuple[int, int] = (0, 0)
        self.color: tuple[int, int, int] = (0, 0, 0)
        self.scale: float = 1.0
        
        # set in DI
        self.game_tree: "Node" = None
        self.screen: pygame.Surface = None
        self.game_state: GameState = None

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

    def add_child(self, new_child: "Node"):
        # adds a child to this node and calls enter tree events if first time added
        if new_child.parent is not None:
            new_child.parent.remove_child(new_child)

        new_child.parent = self
        self.children.append(new_child)

        if new_child.__new_node:
            new_child.__new_node = False
            new_child.enter_tree()
            new_child.game_tree.enter_tree_events(self)

    def remove_child(self, to_remove: "Node"):
        # removes child from this node
        to_remove.parent = None

        if to_remove in self.children:
            _ = self.children.pop(to_remove)

    def reparent(self, new_parent: "Node"):
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
        self.game_tree.exit_tree_events(self)

        for child in self.children:
            child.free()

    def set_visible(self, visible: bool = True):
        self.visible = visible

    def is_visible(self) -> bool:
        if not self.visible:
            return False
        
        if self.parent is not None:
            return self.parent.is_visible()

        return True

    def set_process(self, process: bool = True):
        self.run_process = process

    def move(self, amount: tuple[int, int]):
        if self.rect is not None:
            self.rect.x += amount[0]
            self.rect.y += amount[1]
            self.position = (self.rect.x, self.rect.y)
        else:
            self.position = (self.position[0] + amount[0], self.position[1] + amount[1])
            
        self.move_children(amount)

    def move_children(self, amount: tuple[int, int]):
        for child in self.children:
            if child.rect is not None:
                child.rect.x += amount[0]
                child.rect.y += amount[1]
                child.position = (child.rect.x, child.rect.y)
            else:
                child.position = (child.position[0] + amount[0], child.position[1] + amount[1])
                
            child.move_children(amount)
        
    def move_to(self, position: tuple[int, int]):
        if self.rect is not None:
            self.rect.x = position[0]
            self.rect.y = position[1]
            self.position = (self.rect.x, self.rect.y)
        else:
            self.position = position
            
        self.move_children_to(position)

    def move_children_to(self, position: tuple[int, int]):
        for child in self.children:
            if child.rect is not None:
                child.rect.x = position[0]
                child.rect.y = position[1]
                child.position = (child.rect.x, child.rect.y)
            else:
                child.position = position

            child.move_children_to(position)

    def update_surface(self, force: bool = False):
        if force or (self.surface is None or self.surface.get_size() != self.size):
            self.surface = pygame.Surface(self.size)

        if self.color is not None:
            self.surface.fill(self.color)

        if self.scale != 1.0:
            self.surface = pygame.transform.scale(self.surface, (self.size[0] * self.scale, self.size[1] * self.scale))

        self.set_rect()

    def set_rect(self):
        self.rect = self.surface.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        
    def draw(self):
        if self.surface is not None and self.screen is not None:
            self.screen.blit(self.surface, self.position)

        self.draw_children(self)
        
    def draw_children(self, process_node: "Node"):
        for child in process_node.children:
            if child.visible:
                child.draw()
                self.draw_children(child)
    
    # control methods
    def mouse_entered(self):
        pass

    def mouse_exited(self):
        pass

    def check_mouse_over(self, pos: tuple[int, int]) -> bool:
        if self.visible:
            for child in self.children:
                if child.check_mouse_over(pos):
                    return True
                
        return False
            
    # tree methods
    def process_children(self, process_node: "Node", delta: float):
        for child in process_node.children:
            if child.run_process:
                child.process(delta)

            self.process_children(child, delta)

    def set_screen(self, screen: pygame.Surface):
        self.screen = screen

        for child in self.children:
            child.set_screen(screen)
            
    def enter_tree_events(self, new_node: "Node"):
        pass

    def exit_tree_events(self, removed_node: "Node"):
        pass
