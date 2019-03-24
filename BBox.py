import math
from abc import abstractmethod


class BBox:
    x: float
    y: float

    @abstractmethod
    def is_collision(self, bbox):
        pass

    @abstractmethod
    def distance_to(self, bbox):
        pass


class CircleBBox(BBox):
    """
    circle bounding box
    """

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def is_collision(self, circle):
        return (self.x - circle.x) ** 2 + \
               (self.y - circle.y) ** 2 < (self.radius + circle.radius) ** 2

    def distance_to(self, bbox):
        return math.sqrt((self.x - bbox.x) ** 2 + (self.y - bbox.y) ** 2)

    def __str__(self):
        return '[ x: {}, y: {}, r: {} ]'.format(self.x, self.y, self.radius)

