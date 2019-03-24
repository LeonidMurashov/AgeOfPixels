import pygame
import os
from Constants import *


class Menu:
    coordinates = list()
    coordinates.append(0)
    coordinates.append(800)

    def __init__(self, screen):
        self.main_image = pygame.image.load(os.path.join(IMAGES_FOLDER, 'menu.bmp'))
        self.screen = screen
        self.screen.blit(self.main_image, (self.coordinates[0], self.coordinates[1]))

        pygame.font.init()
        self.comic_sans = pygame.font.SysFont('Comic Sans MS', 30)
        self.text = self.comic_sans.render('select objects and press DELETE!!!', True, (255, 255, 0))

    def render(self):
        self.screen.blit(self.main_image, (self.coordinates[0], self.coordinates[1]))
        self.screen.blit(self.text, (500, 800))

    def render_fps(self, fps):
        if fps < 30:
            text = self.comic_sans.render('FPS: {} - very bad :('.format(fps), True, (255, 255, 0))
        else:
            text = self.comic_sans.render('FPS: {}'.format(fps), True, (255, 255, 0))

        self.screen.blit(text, (0, 0))

    def get_information(self, game_object):
        pass
