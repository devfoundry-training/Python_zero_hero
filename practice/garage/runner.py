from garage.Car import Car
from garage.Garage import Garage

# Example usage
garage = Garage()
my_car = Car(1, "Toyota", "mr2", 1990, 95000, False)
garage.add_vehicle(my_car)

print("Total fix cost:", garage.fix_vehicle())
garage.remove_vehicle(vehicle_id=1)
print("Vehicles after removing car:", len(garage.vehicles))
garage.empty_garage()
print("Vehicles after emptying:", len(garage.vehicles))
