from BBox import *
from factory import *


class DebugObject(GameObject):
    def __init__(self, screen, x, y, color):
        self.s = pygame.Surface((5, 5))
        self.s.fill(color)
        self.x = x
        self.y = y
        self.screen = screen

    def step(self, delta_t):
        pass

    def render(self):
        self.screen.blit(self.s, (self.x, self.y))


class World:
    objects = []
    selected_objects = []
    bbox: CircleBBox
    debug_objects = []

    def __init__(self, screen: pygame.Surface):

        self.objects = [
            Man(screen, self, [300 + i * 50, 300 + j * 50]) for i in range(14) for j in range(14)
        ]
        c = screen.get_size()
        self.bbox = CircleBBox(c[0] / 2, c[1] / 2, c[1] / 2)
        self.screen = screen

    def step(self, elapsed_time):
        for obj in self.objects:
            obj.step(elapsed_time)

    def render(self):
        self.objects.sort(key=lambda x: x.get_y())
        for obj in self.objects:
            obj.render()

        for obj in self.debug_objects:
            obj.render()

    def right_click(self, mouse_pos):
        if len(self.selected_objects) == 0:
            return

        # Creating target position rectangle
        units_num = len(self.selected_objects)
        center = (sum(obj.get_bbox().x for obj in self.selected_objects) / units_num,
                  sum(obj.get_bbox().y for obj in self.selected_objects) / units_num)
        angle = math.atan2(mouse_pos[1] - center[1],
                           mouse_pos[0] - center[0])

        position_distance = 30
        positions = []

        for j in range(int(math.ceil(math.sqrt(units_num))) - 1, -1, -1):
            for i in range(int(math.ceil(math.sqrt(units_num)))):
                x = position_distance * ((j - int(math.ceil(math.sqrt(units_num))) / 2) * math.cos(angle) -
                                         (i - int(math.ceil(math.sqrt(units_num))) / 2) * math.sin(angle)) + mouse_pos[0]
                y = position_distance * ((j - int(math.ceil(math.sqrt(units_num))) / 2) * math.sin(angle) +
                                         (i - int(math.ceil(math.sqrt(units_num))) / 2) * math.cos(angle)) + mouse_pos[1]
                positions.append([x, y])
        # self.debug_objects.clear()
        # self.debug_objects.append(DebugObject(self.screen, positions[0][0], positions[0][1], (255, 25, 255)))

        # Move units
        for i, obj in enumerate(self.selected_objects):
            obj.go_to(positions[i])

    def left_click(self, c):
        pass

    def select_objects(self, rect: pygame.Rect):
        for obj in self.selected_objects:
            obj.set_is_selected(False)
        self.selected_objects = []

        if rect.w < 2 and rect.h < 2:
            # Click case
            mouse_bbox = CircleBBox(rect.x, rect.y, PIXEL_SCALE * 3)
            for obj in self.objects:
                if obj.get_bbox().is_collision(mouse_bbox):
                    self.selected_objects = [obj]
                    obj.set_is_selected(True)
                    return
        else:
            # Rect case
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