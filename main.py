import pygame
import pygame.locals
from pygame.locals import Rect
import os
import math

SCREEN_RECT = Rect(0, 0, 1920, 1080)
IMAGES_FOLDER = 'images'
PIXEL_SCALE = 10

WORLD_GRID = [[ 0 for i in range(100)] for j in range(100)]
WORLD_GRID_SIZE = PIXEL_SCALE

'''
class Physical:
    def __init__(self, bbox : Rect):
        self.bbox = bbox
        pass

    def move(self, x, y):


    def check_collision(self, bbox):
        return self.bbox.colliderect(bbox)
'''

class Man :
    speed = 500
    target = None

    def __init__(self, screen, coordinates):
        self.screen = screen
        self.image = pygame.image.load(os.path.join(IMAGES_FOLDER, 'man.png'))
        self.image = pygame.transform.scale(self.image,
                                            (
                                                self.image.get_size()[0] * PIXEL_SCALE,
                                                self.image.get_size()[1] * PIXEL_SCALE
                                            ))
        self.coordinates = coordinates

    def render(self):
        self.screen.blit(self.image, self.coordinates)

    def animate_go_to(self, delta_t):
        self.coordinates[0] += self.speed * math.sin(
            math.atan2(self.target[0] - self.coordinates[0],
                       self.target[1] - self.coordinates[1])) * delta_t
        self.coordinates[1] += self.speed * math.cos(
            math.atan2(self.target[0] - self.coordinates[0],
                       self.target[1] - self.coordinates[1])) * delta_t

    def step(self, delta_t):
        if self.target is not None:
            self.animate_go_to(delta_t)

    def go_to(self, target):
        self.target = target


def main():
    screen = pygame.display.set_mode(SCREEN_RECT.size, pygame.FULLSCREEN)
    clock = pygame.time.Clock()

    men = [
        Man(screen, [i * 10, i * 10]) for i in range(10)
    ]
    man = Man(screen, [200, 200])

    while True:
        elapsed_time = clock.tick_busy_loop() / 1000

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT or \
                    (event.type == pygame.locals.KEYDOWN and
                     event.key == pygame.locals.K_ESCAPE):
                return
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                man.go_to(pygame.mouse.get_pos())
                for m in men:
                    m.go_to(pygame.mouse.get_pos())

        man.step(elapsed_time)
        man.render()

        for m in men:
            m.step(elapsed_time)
            m.render()

        pygame.display.flip()
        pygame.time.delay(1)
        screen.fill((255, 255, 255))


if __name__ == "__main__":
    import sys

    sys.exit(main())
