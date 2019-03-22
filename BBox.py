class CircleBBox:
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

    def __str__(self):
        return '[ x: {}, y: {}, r: {} ]'.format(self.x, self.y, self.radius)

