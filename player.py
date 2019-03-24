from World import *


class Player:
    _name: str
    _age: str
    _resources = []

    def __init__(self, world, name):
        self.world = world
        self._name = name


class AIPlayer(Player):
    pass


class HumanPlayer(Player):
    def __init__(self, world, name):
        super().__init__(world, name)

    def selection_rect_finished(self, rect):
        self.world.select_objects(self, rect)

    def right_click(self, mouse_pos):
        self.world.move_selected(self, mouse_pos)

    def left_click(self, c):
        pass

    def act(self):
        for i in range(14):
            for j in range(14):
                self.world.create_man(self, [300 + i * 50, 300 + j * 50])
