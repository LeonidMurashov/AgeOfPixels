from abc import ABC, abstractmethod



class Physical(ABC):
    @abstractmethod
    def step(self):
        pass

    @abstractmethod
    def render(self):
        pass


class Worker(Physical):
    @abstractmethod
    def mine(self):
        pass

    @abstractmethod
    def take(self):
        pass


class Warrior(Physical):
    @abstractmethod
    def attack(self):
        pass


class Builder(Physical):
    @abstractmethod
    def build(self):
        pass


class ManWorker(Worker):
    def step(self):
        return 0


class CarWorker(Worker):
    def step(self):
        return 0


class HouseWorker(Worker):
    def step(self):
        return 0


class ManWarrior(Warrior):
    def step(self):
        return 0


class CarWarrior(Warrior):
    def step(self):
        return 0


class HouseWarrior(Warrior):
    def step(self):
        return 0


class ManBuilder(Builder):
    def step(self):
        return 0


class CarBuilder(Builder):
    def step(self):
        return 0


class HouseBuilder(Builder):
    def step(self):
        return 0


class ObjectFactory(ABC):
    def create_workers(self) -> Worker:
        pass

    def create_warriors(self) -> Warrior:
        pass

    def create_builders(self) -> Builder:
        pass


class ManFactory(ObjectFactory):
    def create_workers(self) -> Worker:
        return ManWorker

    def create_warriors(self) -> Warrior:
        return ManWarrior

    def create_builders(self) -> Builder:
        return ManBuilder


class CarFactory(ObjectFactory):
    def create_workers(self) -> Worker:
        return CarWorker

    def create_warriors(self) -> Warrior:
        return CarWarrior

    def create_builders(self) -> Builder:
        return CarBuilder


class HouseFactory(ObjectFactory):
    def create_workers(self) -> Worker:
        return HouseWorker

    def create_warriors(self) -> Warrior:
        return HouseWarrior

    def create_builders(self) -> Builder:
        return HouseBuilder

