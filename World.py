from BBox import *
from factory import *


class World:
    objects = []
    selected_objects = []
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
            if obj.get_is_selected():
                obj.go_to(mouse_pos)

    def left_click(self, c):
        pass

    def select_objects(self, rect: pygame.Rect):
        for obj in self.selected_objects:
            obj.set_is_selected(False)
        self.selected_objects = []

        if rect.w < 2 and rect.h < 2:
            '''
            Click case
            '''
            mouse_bbox = CircleBBox(rect.x, rect.y, PIXEL_SCALE)
            for obj in self.objects:
                if obj._bbox.is_collision(mouse_bbox):
                    self.selected_objects = [obj]
                    obj.set_is_selected(True)
                    return
        else:
            '''
            Rect case
            '''
            for obj in self.objects:
                if rect.collidepoint(obj.get_bbox().x, obj.get_bbox().y):
                    self.selected_objects.append(obj)
                    obj.set_is_selected(True)

    def request_move(self, obj, bbox1):
        if not bbox1.is_collision(self.bbox) and \
                obj.get_bbox().is_collision(self.bbox):
            return False
        '''for i in self.objects:
            bbox2 = i.get_bbox()
            if i != obj and \
                    bbox1.is_collision(bbox2) and \
                    not obj.get_bbox().is_collision(bbox2):
                return False
        '''
        return True
