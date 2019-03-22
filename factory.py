from Menu import *
from Constants import *
from copy import deepcopy
from BBox import *
from abc import ABC, abstractmethod
import pygame
from pygame.locals import Rect
import os
import math
import random
import time


class GameObject(ABC):
    _is_selected: bool = False
    _image: pygame.Surface
    _screen: pygame.Surface

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def step(self, delta_t):
        pass


class Man(GameObject):
    speed = 250
    target = None
    _moving = False

    def __init__(self, screen, world, coordinates):
        self._screen = screen
        self._image = pygame.image.load(os.path.join(IMAGES_FOLDER, 'man.png'))
        self._image = pygame.transform.scale(
            self._image,
            (
                self._image.get_size()[0] * PIXEL_SCALE,
                self._image.get_size()[1] * PIXEL_SCALE
            )
        )
        self._world = world
        self._bbox = CircleBBox(coordinates[0], coordinates[1], 3)

    def render(self):
        self._screen.blit(self._image, (self._bbox.x, self._bbox.y))

    def animate_go_to(self, delta_t):
        new_bbox = deepcopy(self._bbox)
        new_bbox.x += self.speed * math.sin(
            math.atan2(self.target[0] - self._bbox.x,
                       self.target[1] - self._bbox.y)) * delta_t
        new_bbox.y += self.speed * math.cos(
            math.atan2(self.target[0] - self._bbox.x,
                       self.target[1] - self._bbox.y)) * delta_t

        # Check for collisions with others
        if self._world.request_move(self, new_bbox):
            self._bbox = new_bbox

    def step(self, delta_t):
        if self.target is not None:
            self.animate_go_to(delta_t)

    def go_to(self, target):
        self.target = target

    def get_y(self):
        return self._bbox.y

    def get_bbox(self):
        return self._bbox

    def set_is_selected(self, state):
        self._is_selected = state

    def get_is_selected(self):
        return self._is_selected

class Car(GameObject):
    speed: int
    target = None


class Building(GameObject):
    _image: pygame.Surface
    # height = image.get_height()

    def __init__(self, screen):
        self._screen = screen

    def build_it(self):
        for i in range(self.height):
            crop_surf = pygame.transform.chop(self._image, (0, 0, 0, self.height - i))
            self._screen.blit(crop_surf, (440, 440 - i))
            pygame.display.flip()
            self._screen.fill((255, 255, 255))


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


