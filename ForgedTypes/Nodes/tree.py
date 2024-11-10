from ForgedTypes.Nodes.node import Node
import typing

class Tree(Node):
    def __init__(self):
        super().__init__()
        self.on_enter_tree: list[typing.Any] = []
        self.on_exit_tree: list[typing.Any] = []

    def setup(self):
        super().setup()
    
        self.surface = self.screen
        self.rect = self.screen.get_rect()
    

    def enter_tree_events(self, new_node: Node):
        for ev in self.on_enter_tree:
            ev(new_node)

    def exit_tree_events(self, removed_node: Node):
        for ev in self.on_exit_tree:
            ev(removed_node)
