
import typing
import pygame
import Data.PythonDI as PythonDI
from Data.Models.gameState import GameState
from Data.eventHandler import EventHandler
from Data.Nodes import (
    node, 
    tree
)
from Data.Nodes.Controls import control


class NodeFactory:
    def __init__(self, di_container: PythonDI.DIContainer):
        self.di_container: PythonDI.DIContainer = di_container

    def locate_node(self, node_type: type, params: list[typing.Any] = [], setup: bool = True) -> node.Node:
        """Create a Node. 

If setup=False it is recomended to run the .setup() method manually in order to make sure the node is instantiated properly."""
        ret: node.Node = self.di_container.locate(node_type, params)
        ret.screen = self.di_container.locate(pygame.Surface)
        ret.screen_rect = ret.screen.get_rect()
        ret.game_tree = self.di_container.locate(tree.Tree)
        ret.game_state = self.di_container.locate(GameState)

        if setup:
            ret.setup()

        return ret

    def locate_control(self, node_type: type, params: list[typing.Any] = [], setup: bool = True) -> control.Control:
        """Create a Control. 

If setup=False it is recomended to run the .setup() method manually in order to make sure the control is instantiated properly."""
        ret: control.Control = self.locate_node(node_type, params, False)
        ret.event_handler = self.di_container.locate(EventHandler)

        if setup:
            ret.setup()

        return ret
    