from Data.Nodes.node import Node
from Data.Models.queuedEvent import QueuedEvent
import typing
import Data.Helpers.DictHelper as DictHelper

class Tree(Node):
    def __init__(self):
        super().__init__()
        self.name = "Tree"
        self.on_enter_tree: list[typing.Callable[[Node], None]] = []
        self.on_exit_tree: list[typing.Callable[[Node], None]] = []

        self.event_queue: list[QueuedEvent] = []

        self.build_groups: bool = True
        self.node_groups: dict[str, list[Node]] = []

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

    def run_queue_events(self):
        queue = self.event_queue
        self.event_queue = []

        for ev in queue:
            if ev.caller is None or ev.caller.is_valid():
                ev.event()

    def clear_node_groups(self):
        self.build_groups = True
    
    def get_nodes_by_group(self, group: str) -> list[Node]:
        if self.build_groups:
            self.update_node_groups()

        if group in self.node_groups:
            return self.node_groups[group]
        
        return []

    def update_node_groups(self):
        if not self.build_groups:
            return
        
        self.node_groups.clear()
        self.__update_node_groups(self)
        self.build_groups = False

    def __update_node_groups(self, target: Node):
        for child in target.children:
            if child.group is not None and child.group != "":
                DictHelper.add_list(self.node_groups, child.group, child)
            
            self.__update_node_groups(child)