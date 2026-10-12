import unittest

from garage.Car import Car


class TestCar(unittest.TestCase):

    def setUp(self):
        self.my_car = Car(id=1, make="Toyota", model="Corolla", mileage=15000, year=2015, mot=True, fuel_level=80.0)

    # Test initial car attributes
    def test_initiation(self):
        self.assertEqual(self.my_car.make, "Toyota")
        self.assertEqual(self.my_car.model, "Corolla")
        self.assertEqual(self.my_car.mileage, 15000)
        self.assertEqual(self.my_car.year, 2015)
        self.assertTrue(self.my_car.mot)
        self.assertEqual(self.my_car.fuel_level, 80.0)

    # Test setting and getting make property
    def test_set_get_make(self):
        self.my_car.make = "Honda"
        self.assertEqual(self.my_car.make, "Honda")

    # Test setting and getting model property
    def test_set_get_model(self):
        self.my_car.model = "Civic"
        self.assertEqual(self.my_car.model, "Civic")

    # Test setting and getting mileage property
    def test_set_get_mileage(self):
        self.my_car.mileage = 20000
        self.assertEqual(self.my_car.mileage, 20000)

    # Test setting and getting year property
    def test_set_get_year(self):
        self.my_car.year = 2020
        self.assertEqual(self.my_car.year, 2020)

    # Test the string representation (__str__) of the Car object
    def test_str(self):
        expected_str = "Make: Toyota, Model: Corolla, Mileage: 15000 km, Year: 2015, MOT Status: True"
        self.assertEqual(str(self.my_car), expected_str)

    # Test the fuel level attribute (if applicable in the tests)
    def test_fuel_level(self):
        self.assertEqual(self.my_car.fuel_level, 80.0)
        self.my_car.fuel_level = 50.0
        self.assertEqual(self.my_car.fuel_level, 50.0)

    # Test car object creation with another set of values
    def test_car_creation(self):
        another_car = Car(id=2, make="BMW", model="330i", mileage=97000, year=2002, mot=False)
        self.assertEqual(another_car.make, "BMW")
        self.assertEqual(another_car.model, "330i")
        self.assertEqual(another_car.mileage, 97000)
        self.assertEqual(another_car.year, 2002)
        self.assertFalse(another_car.mot)

    # Test MOT status change if applicable
    def test_mot_status(self):
        self.assertTrue(self.my_car.mot)
        self.my_car.mot = False
        self.assertFalse(self.my_car.mot)


if __name__ == "__main__":
    unittest.main()
