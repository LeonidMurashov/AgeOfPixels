import pygame
import pygame.locals
from pygame.locals import Rect


SCREEN_RECT = Rect(0, 0, 1920, 1080)


def main():
    screen = pygame.display.set_mode(SCREEN_RECT.size, pygame.FULLSCREEN)
    clock = pygame.time.Clock()
    while True:
        elapsed_time = clock.tick_busy_loop() / 1000

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT or \
                    (event.type == pygame.locals.KEYDOWN and
                     event.key == pygame.locals.K_ESCAPE):
                return
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pass


        pygame.display.flip()
        screen.fill(1)


if __name__ == "__main__":
    import sys
    sys.exit(main())
