import pygame
import pygame.locals
from pygame.locals import Rect
import os
import math
from abc import ABC, abstractmethod
from factory import *
from Constants import *
from World import *
from SelectionRect import *


def process_events(world: World, selection_rect: SelectionRect, menu: Menu):
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT or \
                (event.type == pygame.locals.KEYDOWN and
                 event.key == pygame.locals.K_ESCAPE):
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:

                selection_rect.start_selection(event.pos)
                world.left_click(event.pos)
            elif event.button == 3:
                world.right_click(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                selection_rect.finish_selection()
        elif event.type == pygame.MOUSEMOTION:
            selection_rect.drag_selection(event.pos)

    return True
        

def main():
    screen = pygame.display.set_mode(SCREEN_RECT.size, pygame.FULLSCREEN)
    pygame.display.set_caption("AgeOfPixels")

    #create fon
    grass = pygame.image.load('images/sand.jpg')
    screen.blit(grass, (0, 0))


    clock = pygame.time.Clock()
    world = World(screen)
    menu = Menu(screen)

    selection_rect = SelectionRect()
    while True:
        elapsed_time = clock.tick_busy_loop() / 1000

        rc = process_events(world, selection_rect, menu)
        if not rc:
            return

        world.step(elapsed_time)
        world.render()
        menu.render()

        if selection_rect.is_selection_active():
            selection_rect.render(screen)

        #if selection_rect.is_selection_finished():
        #    world.select_objects(selection_rect)
        #    selection_rect.mark_as_used()

        pygame.display.flip()
        pygame.time.delay(1)
        screen.blit(grass, (0, 0))


if __name__ == "__main__":
    import sys
    sys.exit(main())
