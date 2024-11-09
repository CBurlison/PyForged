import pygame
from ForgedTypes.Animation.animationFrame import AnimationFrame

BLACK: tuple[int, int, int] = (0, 0, 0)

def create_frame(img: pygame.Surface, color: tuple[int, int, int] = BLACK, frame_duration: float = 1.0) -> AnimationFrame:
    rect = img.get_rect()
    width: int = rect.width
    height: int = rect.height

    frame = pygame.Surface((width, height)).convert_alpha()
    frame.blit(img, (0, 0))
    #frame = pygame.transform.scale(frame, (width * scale, height * scale))
    frame.set_colorkey(color)

    return AnimationFrame(frame, frame_duration)

def create_atlas_frame(img: pygame.Surface, position: tuple[int, int], width: int, height: int, color: tuple[int, int, int] = BLACK, frame_duration: float = 1.0) -> AnimationFrame:
    frame = pygame.Surface((width, height)).convert_alpha()
    frame.blit(img, (0, 0), (position[0], position[1], width, height))
    frame.set_colorkey(color)

    return AnimationFrame(frame, frame_duration)
    