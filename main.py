import pygame
from PythonDI import DIContainer
from eventHandler import EventHandler
from ForgedTypes.Nodes.tree import Tree
from ForgedTypes.gameState import GameState
from Helpers import DIHelper
from Scenes.MainMenu.mainMenu import MainMenu
from nodeFactory import NodeFactory

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
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    di_container.register_instance(pygame.Surface, screen)
    
    game_tree = node_factory.locate_node(Tree)
    di_container.register_instance(Tree, game_tree)

    # Final step before starting game loop
    game_tree.add_child(node_factory.locate_control(MainMenu))
    game_data: GameState = di_container.locate(GameState)
    game_clock.tick(game_data.FPS)

    # Run until the user asks to quit
    while True:
        frame_ticks = game_clock.get_time()

        delta = 0
        if frame_ticks > 0:
            delta = frame_ticks / 1000.0

        game_tree.screen.fill((128, 128, 128))

        if not event_handler.process_frame_events():
            break
       
        game_tree.process_children(game_tree, delta)
        game_tree.check_mouse_over(event_handler.mouse_pos)

        game_tree.draw()

        # Flip the display
        pygame.display.flip()
        game_clock.tick(game_data.FPS)


    # Done! Time to quit.
    pygame.quit()

if __name__ == "__main__":
    main()