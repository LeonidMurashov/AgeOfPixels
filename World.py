from BBox import *
from factory import *
from typing import List
from player import Player


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
    objects: List[GameObject] = []
    alive_objects: List[GameObject] = []
    selected_objects: List[GameObject] = []
    debug_objects: List[GameObject] = []
    dying_objects: List[GameObject] = []

    bbox: CircleBBox
    players: List[Player]

    def __init__(self, screen: pygame.Surface):
        self.screen = screen

        c = screen.get_size()
        self.bbox = CircleBBox(c[0] / 2, c[1] / 2, c[1] / 2)

    def step(self, elapsed_time):
        for obj in self.alive_objects:
            # Filtering out dying objects
            if obj.is_dying():
                self.alive_objects.remove(obj)
                self.dying_objects.append(obj)
                try:
                    self.selected_objects.remove(obj)
                except ValueError:
                    pass
            obj.step(elapsed_time)

        for obj in self.dying_objects:
            if obj.is_dead():
                self.dying_objects.remove(obj)
                self.objects.remove(obj)

    def render(self):
        self.objects.sort(key=lambda x: x.get_y())
        for obj in self.objects:
            obj.render()

        for obj in self.debug_objects:
            obj.render()

    def create_man(self, player, pos):
        man = Man(self.screen, self, pos, player)
        self.objects.append(man)
        self.alive_objects.append(man)

    def move_selected(self, player, mouse_pos):
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
                                         (i - int(math.ceil(math.sqrt(units_num))) / 2) * math.sin(angle)) \
                    + mouse_pos[0]
                y = position_distance * ((j - int(math.ceil(math.sqrt(units_num))) / 2) * math.sin(angle) +
                                         (i - int(math.ceil(math.sqrt(units_num))) / 2) * math.cos(angle)) \
                    + mouse_pos[1]
                positions.append([x, y])
        # self.debug_objects.clear()
        # self.debug_objects.append(DebugObject(self.screen, positions[0][0], positions[0][1], (255, 25, 255)))

        # Move units
        for i, obj in enumerate(self.selected_objects):
            if isinstance(obj, Man) or isinstance(obj, Car):
                obj.go_to(positions[i])

    def select_objects(self, player, rect: pygame.Rect):
        for obj in self.selected_objects:
            obj.set_is_selected(False)
        self.selected_objects = []

        if rect.w < 2 and rect.h < 2:
            # Click case
            mouse_bbox = CircleBBox(rect.x, rect.y, PIXEL_SCALE * 2)
            min_dist = 999999
            min_object = None
            for obj2 in self.alive_objects:
                dist = mouse_bbox.distance_to(obj2.get_bbox())
                if min_dist > dist:
                    min_dist = dist
                    min_object = obj2
            if min_dist <= 20:
                self.selected_objects = [min_object]
                min_object.set_is_selected(True)
        else:
            # Rect case
            for obj in self.alive_objects:
                if rect.collidepoint(obj.get_bbox().x, obj.get_bbox().y):
                    self.selected_objects.append(obj)
                    obj.set_is_selected(True)

    def request_move(self, obj, bbox1):
        if not bbox1.is_collision(self.bbox) and \
                obj.get_bbox().is_collision(self.bbox):
            return False
        '''for i in self.alive_objects:
            bbox2 = i.get_bbox()
            if i != obj and \
                    bbox1.is_collision(bbox2) and \
                    not obj.get_bbox().is_collision(bbox2):
                return False
        '''
        return True

    def find_closest_enemy(self, obj: Man):
        obj_owner = obj.get_owner()
        min_dist = 999999
        min_object = None
        for obj2 in self.alive_objects:
            if obj_owner != obj2.get_owner():
                dist = obj.get_bbox().distance_to(obj2.get_bbox())
                if min_dist > dist:
                    min_dist = dist
                    min_object = obj2
        return min_object if min_dist <= obj.get_line_of_sight() else None

    def remove_selected(self):
        for obj in self.selected_objects:
            obj.set_health(obj.get_health() - 10)

    def create_ore(self):
        self.objects.append(Ore(self.screen, self, [random.randint(350, 1800), random.randint(300, 800)]))

    def check_ore_collision(self, ore):
        for i in self.alive_objects:
            bbox1 = i.get_bbox()
            if ore.get_bbox().is_collision(bbox1):
                return True
