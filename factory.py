from Menu import *
from Constants import *
from copy import deepcopy
from BBox import *
from abc import ABC
import pygame
from pygame.locals import Rect
import os
import math
import random
import time


class GameObject(ABC):
    coordinates: list
    image: pygame.Surface
    screen: pygame.Surface

    def render(self):
        self.screen.blit(self.image, self.coordinates)


class Man(GameObject):
    speed = 250
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
        self.bbox = CircleBBox(coordinates[0], coordinates[1], 3)

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


class Car(GameObject):
    speed: int
    target = None


class Building(GameObject):
    image: pygame.Surface
    # height = image.get_height()

    def __init__(self, screen):
        self.screen = screen

    def build_it(self):
        for i in range(self.height):
            crop_surf = pygame.transform.chop(self.image, (0, 0, 0, self.height - i))
            self.screen.blit(crop_surf, (440, 440 - i))
            pygame.display.flip()
            self.screen.fill((255, 255, 255))


class ManWorker(Man):
    def take_an_object(self):
        return 0


class ManWarrior(Man):
    def attack(self):
        pass


class ManBuilder(Man):
    def build(self):
        pass


class CarWarrior(Car):
    def attack(self):
        pass


class CarWorker(Car):
    def take_an_object(self):
        pass


class BuildingWarrior(Building):
    def attack(self):
        pass


class BuildingWorker(Building):

    def get_ore(self):
        pass


