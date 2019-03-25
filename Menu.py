from factory import *
import pygame
import os
from Constants import *


class Menu:
    coordinates = list()
    coordinates.append(0)
    coordinates.append(800)
    _image = pygame.image.load(os.path.join(IMAGES_FOLDER, 'typeworker.bmp'))
    _image = pygame.transform.scale(
        _image,
        (
            _image.get_size()[0] * PIXEL_SCALE,
            _image.get_size()[1] * PIXEL_SCALE
        )
    )

    _image1 = pygame.image.load(os.path.join(IMAGES_FOLDER, 'typewarrior.bmp'))
    _image1 = pygame.transform.scale(
        _image1,
        (
            _image1.get_size()[0] * PIXEL_SCALE,
            _image1.get_size()[1] * PIXEL_SCALE
        )
    )

    def __init__(self, screen, world):
        self.world = world
        self.main_image = pygame.image.load(os.path.join(IMAGES_FOLDER, 'menu.bmp')).convert()
        self.screen = screen
        self.screen.blit(self.main_image, (self.coordinates[0], self.coordinates[1]))

        pygame.font.init()
        self.comic_sans = pygame.font.SysFont('Comic Sans MS', 30)
        self.text = self.comic_sans.render('select objects and press DELETE!!!', True, (255, 255, 0))

    def render(self):
        self.screen.blit(self.main_image, (self.coordinates[0], self.coordinates[1]))
        self.screen.blit(self.text, (500, 800))
        self.get_information()

    def render_fps(self, fps):
        if fps < 30:
            text = self.comic_sans.render('FPS: {} - very bad :('.format(fps), True, (255, 255, 0))
        else:
            text = self.comic_sans.render('FPS: {}'.format(fps), True, (255, 255, 0))

        self.screen.blit(text, (350, 200))

    def get_information(self):
        selected_type = self.world.get_selected_type()
        if selected_type == ManWorker:
            self.screen.blit(self._image, (500, 800))
        if selected_type == ManWarrior:
            self.screen.blit(self._image1, (500, 800))
