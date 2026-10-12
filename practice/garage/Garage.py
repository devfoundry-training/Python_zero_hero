from garage.Car import Car
from garage.Motorbike import Motorbike


class Garage:
    def __init__(self):
        self.vehicles = []  # List to store vehicles

    def add_vehicle(self, vehicle):
        """Add a vehicle to the garage."""
        self.vehicles.append(vehicle)

    def remove_vehicle(self, vehicle_id=None, vehicle_type=None):
        """Remove a vehicle by its ID or type."""
        if vehicle_id is not None:
            self.vehicles = [v for v in self.vehicles if v.id != vehicle_id]
        elif vehicle_type is not None:
            self.vehicles = [v for v in self.vehicles if not isinstance(v, vehicle_type)]

    def fix_vehicle(self):
        """Iterate through each vehicle and calculate a bill based on its type."""
        bill = 0
        for v in self.vehicles:
            if isinstance(v, Car):
                bill += 100  # Example cost for fixing a car
            elif isinstance(v, Motorbike):
                bill += 50  # Example cost for fixing a motorbike
        return bill

    def empty_garage(self):
        """Remove all vehicles from the garage."""
        self.vehicles.clear()

    def remove_by_type(self, vehicle_type):
        """Remove all vehicles of a certain type."""
        self.vehicles = [v for v in self.vehicles if not isinstance(v, vehicle_type)]
