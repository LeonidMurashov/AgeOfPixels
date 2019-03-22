import pygame


class Menu:
    coordinates = []
    coordinates.append(0)
    coordinates.append(800)

    def __init__(self, screen):
        self.main_image = pygame.image.load('images/menu.bmp')
        self.screen = screen
        self.screen.blit(self.main_image, (self.coordinates[0], self.coordinates[1]))

    def render(self):
        self.screen.blit(self.main_image, (self.coordinates[0], self.coordinates[1]))

    def get_information(self, game_object):
        pass

