from BBox import *
from factory import *


class World:
    objects = []
    bbox: CircleBBox

    def __init__(self, screen: pygame.Surface):

        self.objects = [
            Man(screen, self, [300 + i * 50, 300 + j * 50]) for i in range(14) for j in range(14)
        ]
        c = screen.get_size()
        self.bbox = CircleBBox(c[0] / 2, c[1] / 2, c[1] / 2)

    def step(self, elapsed_time):
        for obj in self.objects:
            obj.step(elapsed_time)

    def render(self):
        self.objects.sort(key=lambda x: x.get_y())
        for obj in self.objects:
            obj.render()

    def right_click(self, mouse_pos):
        for obj in self.objects:
            obj.go_to(mouse_pos)

    def left_click(self, c):
        pass

    def request_move(self, obj, bbox1):
        if not bbox1.is_collision(self.bbox) and \
                obj.get_bbox().is_collision(self.bbox):
            return False
        for i in self.objects:
            bbox2 = i.get_bbox()
            if i != obj and \
                    bbox1.is_collision(bbox2) and \
                    not obj.get_bbox().is_collision(bbox2):
                return False
        return True

