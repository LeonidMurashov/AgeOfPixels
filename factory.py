from Menu import *
from Constants import *
from copy import deepcopy
from BBox import *
from abc import ABC, abstractmethod
import pygame
from pygame.locals import Rect
import os
import math
from player import *


class GameObject(ABC):
    _owner: Player
    _is_selected: bool = False
    _image: pygame.Surface
    _screen: pygame.Surface
    _bbox: BBox
    _health: float
    _max_health: float
    _dying = False

    @abstractmethod
    def render(self):
        pass

    @abstractmethod
    def step(self, delta_t):
        pass

    def get_owner(self):
        return self._owner

    def get_bbox(self):
        return self._bbox

    def set_is_selected(self, state):
        self._is_selected = state

    def get_is_selected(self):
        return self._is_selected

    @abstractmethod
    def is_dead(self):
        pass

    def is_dying(self):
        return self._dying

    def get_health(self):
        return self._health

    def set_health(self, val):
        self._health = val


class Man(GameObject):
    _speed = 150
    _line_of_sight = 200
    _target = None
    _moving = False
    _chasing_object: GameObject = None
    _sprite_offset = 0
    _bbox: CircleBBox
    _step_counter = 0
    _max_health = 100
    _health = _max_health
    _death_animation_steps = 60

    def __init__(self, screen, world, coordinates, owner):
        self._screen = screen
        self._world = world
        self._owner = owner

        self._image = pygame.image.load(os.path.join(IMAGES_FOLDER, 'man.png'))
        self._image = pygame.transform.scale(
            self._image,
            (
                self._image.get_size()[0] * PIXEL_SCALE,
                self._image.get_size()[1] * PIXEL_SCALE
            )
        )
        self._bbox = CircleBBox(coordinates[0] + self._image.get_width() / 2,
                                coordinates[1] + self._image.get_height() / 2,
                                3)
        self._health = random.randint(1, 100)

    def render(self):
        if not self._dying:
            # Draw white ellipse underneath unit
            if self._is_selected:
                pygame.draw.ellipse(self._screen,
                                    (255, 255, 255),
                                    Rect(
                                        self._bbox.x - (self._image.get_width() * 1.6 / 2),
                                        self._bbox.y + self._image.get_height() / 2 - 8 / 2 + self._sprite_offset,
                                        self._image.get_width() * 1.6,
                                        8),
                                    2)

            # Draw unit
            self._screen.blit(self._image,
                              (self._bbox.x - self._image.get_width() / 2,
                               self._bbox.y + self._sprite_offset - self._image.get_height() / 2))

            # Draw health bar
            if self._is_selected:
                # Red part
                pygame.draw.rect(self._screen,
                                 (255, 0, 0),
                                 Rect(self._bbox.x - 30 / 2,
                                      self._bbox.y - self._image.get_height() / 2 - 10,
                                      30,
                                      2))
                # Green part
                pygame.draw.rect(self._screen,
                                 (0, 255, 0),
                                 Rect(self._bbox.x - 30 / 2,
                                      self._bbox.y - self._image.get_height() / 2 - 10,
                                      30 * (self._health / self._max_health),
                                      2))
        elif self._dying:
            # Draw unit
            self._image.fill((255, 255, 255, 220), None, pygame.BLEND_RGBA_MULT)

            self._screen.blit(self._image,
                              (self._bbox.x - self._image.get_width() / 2,
                               self._bbox.y + self._sprite_offset - self._image.get_height() / 2))
            self._death_animation_steps -= 1

    def animate_go_to(self, delta_t):
        if self._moving:
            new_bbox = deepcopy(self._bbox)
            new_bbox.x += self._speed * math.sin(
                math.atan2(self._target[0] - self._bbox.x,
                           self._target[1] - self._bbox.y)) * delta_t
            new_bbox.y += self._speed * math.cos(
                math.atan2(self._target[0] - self._bbox.x,
                           self._target[1] - self._bbox.y)) * delta_t

            # Moving ended
            target_bbox = CircleBBox(self._target[0], self._target[1], 0)
            if self._bbox.distance_to(target_bbox) < self._speed * delta_t:
                self._moving = False

            # Check for collisions with world bounds
            if self._world.request_move(self, new_bbox):
                self._bbox = new_bbox

                # Jumping animation
                self._sprite_offset = 5 if self._sprite_offset == 0 else 0

    def step(self, delta_t):
        if self._health > 0:
            if self._moving:
                if self._chasing_object is not None:
                    # Check if still visible
                    if self._chasing_object.get_bbox().distance_to(self._bbox) > self._line_of_sight * 2:
                        self._chasing_object = None
                        return
                    self._target = [self._chasing_object.get_bbox().x, self._chasing_object.get_bbox().y]
                self.animate_go_to(delta_t)
            else:
                if self._step_counter == 10:
                    enemy = self._world.find_closest_enemy(self)
                    if enemy is not None:
                        self._chasing_object = enemy
                        self._moving = True
        else:
            # Dying phase on
            if not self._dying:
                # TODO: Death sound, etc..
                self._dying = True

        self._step_counter = 0 if self._step_counter == 10 else self._step_counter + 1

    def go_to(self, target):
        self._target = target
        self._chasing_object = None
        self._moving = True

    def get_y(self):
        return self._bbox.y

    def get_line_of_sight(self):
        return self._line_of_sight

    def is_dead(self):
        return self._death_animation_steps <= 0


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
