from Data.Nodes.node import Node
from Data.Nodes.Controls.control import Control
from Data.Factories.nodeFactory import NodeFactory

class SceneManager(Node):
    def __init__(self, node_factory: NodeFactory):
        super().__init__()
        self.name = "SceneManager"

        self.node_factory = node_factory
        self.__scene_node: Node = None

    def more_setup(self):
        self.__scene_node = self.game_tree.get_node("SceneNode")

    def change_scene(self, scene: type) -> Node:
        free_nodes = self.__scene_node.children.copy()

        for child in free_nodes:
            child.free()

        return self.add_scene(scene)

    def add_scene(self, scene: type) -> Node:
        if issubclass(scene, Control):
            new_scene = self.node_factory.locate_control(scene)
            self.__scene_node.add_child(new_scene)
        else:
            new_scene = self.node_factory.locate_node(scene)
            self.__scene_node.add_child(new_scene)
        
        return new_scene