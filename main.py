import pygame
from PythonDI import DIContainer
from EventHandler import EventHandler
from ForgedTypes.tree import Tree
from ForgedTypes.game_data import GameData
from Helpers import DIHelper
from Scenes.MainMenu.MainMenu import MainMenu

def main():
    pygame.init()

    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080

    FPS = 60
    game_clock = pygame.time.Clock()
    game_clock.tick(FPS)

    di_container = DIContainer()
    di_container.register_instance(DIContainer, di_container)
    di_container.register_instance(pygame.time.Clock, game_clock)
    di_container.register_instance(GameData)

    DIHelper.register_nodes(di_container)

    event_handler = EventHandler()
    di_container.register_instance(EventHandler, event_handler)

    # Set up the drawing window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    di_container.register_instance(pygame.Surface, screen)
    
    game_tree = Tree(screen)
    di_container.register_instance(Tree, game_tree)

    # Final step before starting game loop
    game_tree.add_child(di_container.locate(MainMenu))
    game_clock.tick(FPS)

    # Run until the user asks to quit
    while True:
        frame_ticks = game_clock.get_time()

        delta = 0
        if frame_ticks > 0:
            delta = frame_ticks / 1000.0

        game_tree.screen.fill((128, 128, 128))

        if not event_handler.process_frame_events():
            break
       
        game_tree.process(delta)

        game_tree.draw()

        # Flip the display
        pygame.display.flip()
        game_clock.tick(FPS)


    # Done! Time to quit.
    pygame.quit()

if __name__ == "__main__":
    main()