from abc import ABC
import pygame
from pygame.locals import Rect
import os
import math
import random
import time


class Renderable(ABC):
    coordinates: list
    image: pygame.Surface
    screen: pygame.Surface

    def render(self):
        self.screen.blit(self.image, self.coordinates)


class Man(Renderable):
    speed = 500
    target = None

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

    def get_y(self):
        return self.coordinates[1]


class Car(Renderable):
    speed: int
    target = None


class Building(Renderable):
    image : pygame.Surface
    height = image.get_height()

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


