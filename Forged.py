import pygame
from Data.PythonDI import DIContainer
from Data.eventHandler import EventHandler
from Data.Nodes.tree import Tree
from Data.Models.gameState import GameState
from Data.Helpers import DIHelper
from Data.Scenes.MainMenu.mainMenu import MainMenu
from Data.Scenes.FpsCounter.fpsCounter import FpsCounter
from Data.Factories.nodeFactory import NodeFactory
from Data.GameData.imageStore import ImageStore
from Data.GameData.animationStore import AnimationStore
from Data.Nodes.node import Node
from Data.Nodes.Controls.Sprites.button import Button
from Data.Nodes.Controls.control import AnchorPoint

def is_button(search_node: Node) -> bool:
    return isinstance(search_node, Button)

def update_groups(event_handler: EventHandler, game_tree: Tree):
    if event_handler.build_button_groups:
        event_handler.update_button_groups(game_tree.get_nodes(is_button))

    game_tree.update_node_groups()

def main():
    pygame.init()
    pygame.font.init()

    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    
    game_clock = pygame.time.Clock()
    game_clock.tick(60)
    
    di_container = DIContainer()
    di_container.register_instance(DIContainer, di_container)

    di_container.register_instance(NodeFactory)
    node_factory: NodeFactory = di_container.locate(NodeFactory)

    di_container.register_instance(pygame.time.Clock, game_clock)
    di_container.register_instance(GameState)

    DIHelper.register_nodes(di_container)

    event_handler = EventHandler()
    di_container.register_instance(EventHandler, event_handler)

    # Set up the drawing window
    di_container.register_instance(pygame.Surface, pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)))
    di_container.register_instance(ImageStore, ImageStore())
    di_container.register_instance(AnimationStore)
    _ = di_container.locate(AnimationStore)
    
    game_tree = node_factory.locate_node(Tree)
    di_container.register_instance(Tree, game_tree)

    def update_button_groups():
        event_handler.update_button_groups(game_tree.get_nodes(is_button))

    # EventHandler doesnt have access to the tree for things. Give it what it needs here
    event_handler.update_button_groups_func = update_button_groups

    # Final step before starting game loop
    scene_node: Node = node_factory.locate_control(Node)
    scene_node.name = "SceneNode"
    game_tree.add_child(scene_node)
    scene_node.add_child(node_factory.locate_control(MainMenu))
    game_data: GameState = di_container.locate(GameState)
    
    fps_label: FpsCounter = node_factory.locate_control(FpsCounter)
    fps_label.transform.position = (SCREEN_WIDTH/2, 60)
    fps_label.transform.size = (SCREEN_WIDTH, 60)
    fps_label.anchor_point = AnchorPoint.Center
    game_tree.add_child(fps_label)

    game_tree.screen.fill((128, 128, 128))
    pygame.display.flip()
    game_clock.tick(game_data.FPS)

    # Get rid of all of the references we no longer need
    node_factory = None
    scene_node = None

    update_groups(event_handler, game_tree)

    # Main game loop
    while True:
        game_data.delta = calc_delta_sec(game_clock.get_time())
        game_tree.screen.fill((128, 128, 128))

        if not event_handler.process_frame_events():
            break
       
        game_tree.check_mouse_over(event_handler.mouse_pos)
        game_tree.process_children(game_tree, game_data.delta)

        game_tree.run_queue_events()

        update_groups(event_handler, game_tree)

        game_tree.draw()

        # Flip the display
        pygame.display.update()
        game_clock.tick(game_data.FPS)


    # Done! Time to quit.
    pygame.quit()

def calc_delta_sec(ms):
    if ms > 0:
        return ms / 1000.0
    
    return ms

if __name__ == "__main__":
    main()