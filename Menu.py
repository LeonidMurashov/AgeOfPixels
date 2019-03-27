from factory import *
import pygame
import os
from Constants import *


class Menu:
    coordinates = list()
    coordinates.append(0)
    coordinates.append(750)

    def __init__(self, screen, world):
        self.world = world
        self.main_image = pygame.image.load(os.path.join(IMAGES_FOLDER, 'menu.bmp')).convert()
        self._imageMW = pygame.image.load(os.path.join(IMAGES_FOLDER, 'typeworker.bmp')).convert()
        self._imageMWar = pygame.image.load(os.path.join(IMAGES_FOLDER, 'typewarrior.bmp')).convert()
        self._imageMB = pygame.image.load(os.path.join(IMAGES_FOLDER, 'typebuilder.bmp')).convert()
        self.screen = screen
        self.screen.blit(self.main_image, (self.coordinates[0], self.coordinates[1]))

        pygame.font.init()
        self.comic_sans = pygame.font.SysFont('Comic Sans MS', 30)
        self.text = self.comic_sans.render('Type:', True, (255, 255, 0))

    def render(self):
        self.screen.blit(self.main_image, (self.coordinates[0], self.coordinates[1]))
        self.screen.blit(self.text, (400, 800))
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
            self.screen.blit(self._imageMW, (500, 770))
        if selected_type == ManWarrior:
            self.screen.blit(self._imageMWar, (500, 770))
        if selected_type == ManBuilder:
            self.screen.blit(self._imageMB, (500, 770))
