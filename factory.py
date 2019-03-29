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

    @abstractmethod
    def is_dead(self):
        pass

    def get_owner(self):
        return self._owner

    def get_bbox(self):
        return self._bbox

    def set_is_selected(self, state):
        self._is_selected = state

    def get_is_selected(self):
        return self._is_selected

    def is_dying(self):
        return self._dying

    def get_health(self):
        return self._health

    def set_health(self, val):
        self._health = val


class ManFactory:
    def __init__(self, screen, world):
        self._screen = screen
        self._world = world

    def create_man(self, name, player, coordinates):
        if name == "ManWorker":
            return ManWorker(self._screen, self._world, coordinates, player)
        if name == "ManWarrior":
            return ManWarrior(self._screen, self._world, coordinates, player)
        if name == "ManBuilder":
            return ManBuilder(self._screen, self._world, coordinates, player)


class CarFactory:
    def __init__(self, screen, world):
        self._screen = screen
        self._world = world

    def create_car(self, name, player, coordinates):
        if name == "CarWorker":
            return CarWorker(self._screen, self._world, coordinates, player)
        if name == "CarWarrior":
            return CarWarrior(self._screen, self._world, coordinates, player)


class BuildingFactory:
    def __init__(self, screen, world):
        self._screen = screen
        self._world = world

    def create_building(self, name, player, coordinates):
        if name == "BuildingWorker":
            return BuildingWorker(self._screen, self._world, coordinates, player)
        if name == "BuildingWarrior":
            return BuildingWarrior(self._screen, self._world, coordinates, player)


class Man(GameObject, ABC):
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
    _sprite_name: str
    _time = 0

    def __init__(self, screen, world, coordinates, owner):
        self._screen = screen
        self._world = world
        self._owner = owner

        self._image = pygame.image.load(os.path.join(IMAGES_FOLDER, self._sprite_name)).convert()
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
                                        10),
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
                self._sprite_offset = 2 * ((self._time * 20) % 5)

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

        self._time += delta_t
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
    _speed = 400
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
    _sprite_name: str

    def __init__(self, screen, world, coordinates, owner):
        self._screen = screen
        self._world = world
        self._owner = owner

        self._image = pygame.image.load(os.path.join(IMAGES_FOLDER, self._sprite_name)).convert_alpha()
        self._image = pygame.transform.scale(
            self._image,
            (
                self._image.get_size()[0] * PIXEL_SCALE,
                self._image.get_size()[1] * PIXEL_SCALE
            )
        )
        self._bbox = CircleBBox(coordinates[0] + self._image.get_width() / 2,
                                coordinates[1] + self._image.get_height() / 2,
                                100)
        self._health = random.randint(1, 100)

    def render(self):
        if not self._dying:
            # Draw white ellipse underneath unit
            if self._is_selected:
                pygame.draw.ellipse(self._screen,
                                    (255, 255, 255),
                                    Rect(
                                        self._bbox.x - (self._image.get_width() * 1.2 / 2),
                                        self._bbox.y + self._image.get_height() / 2 - 8 / 2 + self._sprite_offset,
                                        self._image.get_width() * 1.2,
                                        12),
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


class Building(GameObject):
    _image: pygame.Surface
    _sprite_name: str

    def __init__(self, screen, world, coordinates, owner):
        self._screen = screen
        self._world = world
        self._owner = owner

        self._image = pygame.image.load(os.path.join(IMAGES_FOLDER, self._sprite_name)).convert_alpha()
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

    def step(self, delta_t):
        pass

    def is_dead(self):
        pass

    def render(self):
        self._screen.blit(self._image,
                          (self._bbox.x - self._image.get_width() / 2,
                           self._bbox.y - self._image.get_height() / 2))

    def get_y(self):
        return self._bbox.y

    '''def build_it(self):
            for i in range(self.height):
                crop_surf = pygame.transform.chop(self._image, (0, 0, 0, self.height - i))
                self._screen.blit(crop_surf, (440, 440 - i))
                pygame.display.flip()
                self._screen.fill((255, 255, 255))'''


class ManWorker(Man):
    _sprite_name = 'worker.bmp'

    def take_an_object(self):
        pass


class ManWarrior(Man):
    _sprite_name = 'warrior.bmp'

    def attack(self):
        pass


class ManBuilder(Man):
    _sprite_name = 'builder.bmp'

    def build(self):
        pass


class CarWarrior(Car):
    _sprite_name = 'carwar.png'

    def attack(self):
        pass


class CarWorker(Car):
    _sprite_name = 'car.png'

    def take_an_object(self):
        pass


class BuildingWarrior(Building):
    _sprite_name = "warbuilding.png"

    def attack(self):
        pass


class BuildingWorker(Building):
    _sprite_name = "building.png"

    def get_ore(self):
        pass


class Ore(GameObject):
    _moving = False
    _chasing_object: GameObject = None
    _bbox: CircleBBox

    def __init__(self, screen, world, coordinates):
        self._screen = screen
        self._world = world

        self._image = pygame.image.load(os.path.join(IMAGES_FOLDER, 'ore.png')).convert()
        self._image = pygame.transform.scale(
            self._image,
            (
                self._image.get_size()[0] * PIXEL_SCALE,
                self._image.get_size()[1] * PIXEL_SCALE
            )
        )

        self._bbox = CircleBBox(coordinates[0] + self._image.get_width() / 2,
                                coordinates[1] + self._image.get_height() / 2,
                                10)

    def render(self):
        if self._world.check_ore_collision(self):
            self._world.objects.remove(self)
            return
        self._screen.blit(self._image, (self._bbox.x, self._bbox.y))

    def step(self, delta_t):
        pass

    def is_dead(self):
        pass

    def get_y(self):
        return self._bbox.y
