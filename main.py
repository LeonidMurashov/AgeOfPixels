import pygame.locals
from World import *
from SelectionRect import *
import sys
from Menu import *

import ctypes
from ctypes import windll

def process_events(world: World, player: HumanPlayer, selection_rect: SelectionRect, menu: Menu):
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT or \
                (event.type == pygame.locals.KEYDOWN and
                 event.key == pygame.locals.K_ESCAPE):
            return False
        elif event.type == pygame.locals.KEYDOWN:
            if event.key == pygame.locals.K_DELETE:
                player.delete_button()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                selection_rect.start_selection(event.pos)
                player.left_click(event.pos)
            elif event.button == 3:  # Right mouse button
                player.right_click(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                selection_rect.finish_selection()
        elif event.type == pygame.MOUSEMOTION:
            selection_rect.drag_selection(event.pos)

    return True


def main():
    global SCREEN_RECT

    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (0, -1)
    pygame.init()

    info_object = pygame.display.Info()
    SCREEN_RECT = Rect(0, 0, info_object.current_w, info_object.current_h)

    ctypes.windll.user32.SetProcessDPIAware()
    true_res = (windll.user32.GetSystemMetrics(0), windll.user32.GetSystemMetrics(1))
    screen: pygame.Surface = pygame.display.set_mode(true_res, pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)

    pygame.display.set_caption("AgeOfPixels")

    # Create background
    grass = pygame.image.load(os.path.join(IMAGES_FOLDER, 'sand.jpg')).convert()

    clock = pygame.time.Clock()
    world = World(screen)
    menu = Menu(screen, world, SCREEN_RECT)
    selection_rect = SelectionRect()

    players = [HumanPlayer(world, 'Player'), HumanPlayer(world, 'Player1')]
    players[0].act()
    # players[0].create_army(1)
    # players[1].create_army(1)

    while True:
        elapsed_time = clock.tick_busy_loop() / 1000

        rc = process_events(world, players[0], selection_rect, menu)
        if not rc:
            return

        world.step(elapsed_time)
        world.render()
        menu.render()

        if selection_rect.is_selection_active():
            selection_rect.render(screen)

        if selection_rect.is_selection_finished():
            players[0].selection_rect_finished(selection_rect.get_rect())
            selection_rect.mark_as_used()

        menu.render_fps(int(clock.get_fps()))

        mouse_pos = pygame.mouse.get_pos()

        pygame.display.flip()
        pygame.time.delay(1)
        screen.fill(1)
        screen.blit(grass, (0, 0))


if __name__ == "__main__":
    sys.exit(main())
