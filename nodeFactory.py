from ForgedTypes.Nodes.Controls import control
from ForgedTypes.gameState import GameState
import PythonDI
import typing
import pygame
from eventHandler import EventHandler
from ForgedTypes.Nodes import (
    node, 
    tree
)

class NodeFactory:
    def __init__(self, di_container: PythonDI.DIContainer):
        self.di_container: PythonDI.DIContainer = di_container

    def locate_node(self, node_type: type, params: list[typing.Any] = [], setup: bool = True) -> node.Node:
        ret: node.Node = self.di_container.locate(node_type, params)
        ret.screen = self.di_container.locate(pygame.Surface)
        ret.game_tree = self.di_container.locate(tree.Tree)
        ret.game_state = self.di_container.locate(GameState)

        if setup:
            ret.setup()

        return ret

    def locate_control(self, node_type: type, params: list[typing.Any] = [], setup: bool = True) -> control.Control:
        ret: control.Control = self.locate_node(node_type, params, False)
        ret.event_handler = self.di_container.locate(EventHandler)

        if setup:
            ret.setup()

        return ret
    