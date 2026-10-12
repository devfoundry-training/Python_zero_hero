# ============================================================
# Abstraction - Abstract Base Classes (ABC)
# ============================================================

from abc import ABC, abstractmethod


class Vehicle(ABC):
    """An Abstract Vehicle class"""

    def __init__(self, make, model):
        self.make = make
        self.model = model

    @abstractmethod
    def start_engine(self):
        """Abstract method to start the engine"""

    @abstractmethod
    def stop_engine(self):
        """Abstract method to stop the engine"""

    @abstractmethod
    def honk(self):
        """Abstract method to honk"""


class Car(Vehicle):
    __count = 0

    def __init__(self, make, model, num_doors):
        super().__init__(make, model)
        self.num_doors = num_doors
        Car.__count += 1

    @classmethod
    def get_car_count(cls):
        return cls.__count

    def start_engine(self):
        print(f"The engine of the {self.make} {self.model} car is starting.")

    def stop_engine(self):
        print(f"The engine of the {self.make} {self.model} car is stopping.")

    def honk(self):
        print(f"The {self.make} {self.model} car honks: Beep beep!")
