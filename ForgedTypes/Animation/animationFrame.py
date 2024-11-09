import pygame

class AnimationFrame:
    BLACK: tuple[int, int, int] = (0, 0, 0)

    def __init__(self, frame: pygame.Surface, frame_duration: float = 1.0):
        self.frame: pygame.Surface = frame
        self.frame_duration: float = frame_duration
