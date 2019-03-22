import pygame
import pygame.locals
from pygame.locals import Rect
import os
import math
from abc import ABC, abstractmethod
from copy import deepcopy

SCREEN_RECT = Rect(0, 0, 1920, 1080)
IMAGES_FOLDER = 'images'
PIXEL_SCALE = 10

WORLD_GRID = [[0 for i in range(100)] for j in range(100)]
WORLD_GRID_SIZE = PIXEL_SCALE


class SelectionRect:
    rect: pygame.Rect = pygame.Rect((0, 0, 0, 0))
    is_active = False


class CircleBBox:
    """
    circle bounding box
    """

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def is_collision(self, circle):
        return (self.x - circle.x) ** 2 + \
               (self.y - circle.y) ** 2 < (self.radius + circle.radius) ** 2

    def __str__(self):
        return '[ x: {}, y: {}, r: {} ]'.format(self.x, self.y, self.radius)


class World:
    objects = []
    bbox: CircleBBox

    def __init__(self, screen: pygame.Surface):

        self.objects = [
            Man(screen, self, [300 + i * 50, 300 + j * 50]) for i in range(14) for j in range(14)
        ]
        self.objects.append(Man(screen, self, [200, 200]))
        c = screen.get_size()
        self.bbox = CircleBBox(c[0] / 2, c[1] / 2, c[1] / 2)

    def step(self, elapsed_time):
        for obj in self.objects:
            obj.step(elapsed_time)

    def render(self):
        self.objects.sort(key=lambda x: x.get_y())
        for obj in self.objects:
            obj.render()

    def right_click(self, mouse_pos):
        for obj in self.objects:
            obj.go_to(mouse_pos)

    def left_click(self, c):
        pass

    def request_move(self, obj, bbox1):
        if not bbox1.is_collision(self.bbox) and \
                obj.get_bbox().is_collision(self.bbox):
            return False
        for i in self.objects:
            bbox2 = i.get_bbox()
            if i != obj and \
                    bbox1.is_collision(bbox2) and \
                    not obj.get_bbox().is_collision(bbox2):
                return False
        return True


class GameObject(ABC):
    image: pygame.Surface
    image_coordinates: list
    bbox: CircleBBox

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def step(self, delta_t):
        pass


class Man(GameObject):
    speed = 500
    target = None

    def __init__(self, screen, world, coordinates):
        self.screen = screen
        self.image = pygame.image.load(os.path.join(IMAGES_FOLDER, 'man.png'))
        self.image = pygame.transform.scale(
            self.image,
            (
                self.image.get_size()[0] * PIXEL_SCALE,
                self.image.get_size()[1] * PIXEL_SCALE
            )
        )
        self.world = world
        self.bbox = CircleBBox(coordinates[0], coordinates[1], 10)

    def render(self):
        self.screen.blit(self.image, (self.bbox.x, self.bbox.y))

    def animate_go_to(self, delta_t):
        new_bbox = deepcopy(self.bbox)
        new_bbox.x += self.speed * math.sin(
            math.atan2(self.target[0] - self.bbox.x,
                       self.target[1] - self.bbox.y)) * delta_t
        new_bbox.y += self.speed * math.cos(
            math.atan2(self.target[0] - self.bbox.x,
                       self.target[1] - self.bbox.y)) * delta_t

        # Check for collisions with others
        if self.world.request_move(self, new_bbox):
            self.bbox = new_bbox

    def step(self, delta_t):
        if self.target is not None:
            self.animate_go_to(delta_t)

    def go_to(self, target):
        self.target = target

    def get_y(self):
        return self.bbox.y

    def get_bbox(self):
        return self.bbox


def process_events(world: World, selection_rect: SelectionRect):
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT or \
                (event.type == pygame.locals.KEYDOWN and
                 event.key == pygame.locals.K_ESCAPE):
            return False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                selection_rect.is_active = True
                selection_rect.rect.x = event.pos[0]
                selection_rect.rect.y = event.pos[1]
                selection_rect.rect.h = 1
                selection_rect.rect.w = 1
                world.left_click(event.pos)
            elif event.button == 3:
                world.right_click(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                selection_rect.is_active = False
                selection_rect.rect.h = event.pos[1] - selection_rect.rect.y
                selection_rect.rect.w = event.pos[0] - selection_rect.rect.x
        elif event.type == pygame.MOUSEMOTION:
            selection_rect.rect.h = event.pos[1] - selection_rect.rect.y
            selection_rect.rect.w = event.pos[0] - selection_rect.rect.x

    return True

'''            if selection_rect.rect.w < 0:
                selection_rect.rect.x += selection_rect.rect.w
                selection_rect.rect.w *= -1
            if selection_rect.rect.h < 0:
                selection_rect.rect.y += selection_rect.rect.h
                selection_rect.rect.h *= -1'''
def main():
    screen = pygame.display.set_mode(SCREEN_RECT.size, pygame.FULLSCREEN)
    pygame.display.set_caption("AgeOfPixels")
    clock = pygame.time.Clock()

    world = World(screen)
    selection_rect = SelectionRect()
    while True:
        elapsed_time = clock.tick_busy_loop() / 1000

        rc = process_events(world, selection_rect)
        if not rc:
            return

        world.step(elapsed_time)
        world.render()

        if selection_rect.is_active:
            if selection_rect.rect.w < 0:
                selection_rect.rect.x += selection_rect.rect.w
                selection_rect.rect.w *= -1
            if selection_rect.rect.h < 0:
                selection_rect.rect.y += selection_rect.rect.h
                selection_rect.rect.h *= -1

            s = pygame.Surface((selection_rect.rect.w, selection_rect.rect.h), pygame.SRCALPHA)
            s.fill((0, 0, 255, 128))
            screen.blit(s, (selection_rect.rect.x, selection_rect.rect.y))

        pygame.display.flip()
        pygame.time.delay(1)
        screen.fill((255, 255, 255))


if __name__ == "__main__":
    import sys
    sys.exit(main())
