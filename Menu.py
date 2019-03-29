from factory import *
import pygame
import os
from Constants import *
from typing import Tuple


class Menu:
    coordinates: Tuple[int]

    def __init__(self, screen, world, screen_rect):
        self.world = world
        self.main_image: pygame.Surface = pygame.image.load(os.path.join(IMAGES_FOLDER, 'menu.bmp')).convert()
        self._imageMW = pygame.image.load(os.path.join(IMAGES_FOLDER, 'typeworker.bmp')).convert()
        self._imageMWar = pygame.image.load(os.path.join(IMAGES_FOLDER, 'typewarrior.bmp')).convert()
        self._imageMB = pygame.image.load(os.path.join(IMAGES_FOLDER, 'typebuilder.bmp')).convert()
        self._imageCW = pygame.image.load(os.path.join(IMAGES_FOLDER, 'typecarworker.png')).convert()
        self._imageCWar = pygame.image.load(os.path.join(IMAGES_FOLDER, 'typecarwar.png')).convert()
        self._imageBW = pygame.image.load(os.path.join(IMAGES_FOLDER, 'typewarbuilding.png')).convert()
        self.screen = screen
        self.coordinates_type = [200, screen_rect.h - 100]

        pygame.font.init()
        self.comic_sans = pygame.font.SysFont('Comic Sans MS', 30)
        self.text = self.comic_sans.render('Type:', True, (255, 255, 0))
        self.coordinates = (0, screen_rect.h - self.main_image.get_height())
        self.screen.blit(self.main_image, (self.coordinates[0], self.coordinates[1]))

    def render(self):
        self.screen.blit(self.main_image, (self.coordinates[0], self.coordinates[1]))
        self.screen.blit(self.text, (100, 1000))
        self.get_information()

    def render_fps(self, fps):
        if fps < 30:
            text = self.comic_sans.render('FPS: {} - very bad :('.format(fps), True, (255, 255, 0))
        else:
            text = self.comic_sans.render('FPS: {}'.format(fps), True, (255, 255, 0))

        self.screen.blit(text, (10, 0))

    def get_information(self):
        selected_type = self.world.get_selected_type()
        if selected_type == ManWorker:
            self.screen.blit(self._imageMW, self.coordinates_type)
        if selected_type == ManWarrior:
            self.screen.blit(self._imageMWar, self.coordinates_type)
        if selected_type == ManBuilder:
            self.screen.blit(self._imageMB, self.coordinates_type)
        if selected_type == CarWarrior:
            self.screen.blit(self._imageCWar, self.coordinates_type)
        if selected_type == CarWorker:
            self.screen.blit(self._imageCW, self.coordinates_type)
        if selected_type == BuildingWarrior:
            self.screen.blit(self._imageBW, self.coordinates_type)
