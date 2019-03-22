import pygame
from copy import deepcopy


class SelectionRect:
    rect: pygame.Rect = pygame.Rect((0, 0, 0, 0))
    __is_active = False
    __is_finished = False

    tracked_corner = [0, 0]
    '''
    how tracked corner is represented 
     TT | FT
    --------
     TF | FF
    '''

    def start_selection(self, pos):
        self.__is_active = True
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.rect.h = 1
        self.rect.w = 1
        self.tracked_corner = [0, 0]

    def finish_selection(self):
        self.__is_active = False
        self.__is_finished = True

    def drag_selection(self, pos):
        self.rect.w = pos[0] - self.rect.x
        self.rect.h = pos[1] - self.rect.y

        if self.rect.w < 0 and not self.tracked_corner[0]:
            self.tracked_corner[0] ^= 1
        if self.rect.w > 0 and self.tracked_corner[0]:
            self.tracked_corner[0] ^= 1
        if self.rect.h < 0 and not self.tracked_corner[1]:
            self.tracked_corner[1] ^= 1
        if self.rect.h > 0 and self.tracked_corner[1]:
            self.tracked_corner[1] ^= 1

    def get_rect(self):
        rect = deepcopy(self.rect)
        if self.tracked_corner[0]:
            rect.x += self.rect.w
            rect.w *= -1
        if self.tracked_corner[1]:
            rect.y += self.rect.h
            rect.h *= -1
        return rect

    def is_selection_finished(self):
        return self.__is_finished

    def is_selection_active(self):
        return self.__is_active

    def mark_as_used(self):
        self.__is_finished = False

    def render(self, screen):
        s = pygame.Surface((self.get_rect().w, self.get_rect().h), pygame.SRCALPHA)
        s.fill((0, 0, 255, 128))
        screen.blit(s, (self.get_rect().x, self.get_rect().y))
