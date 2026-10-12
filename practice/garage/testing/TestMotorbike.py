import unittest

from garage.Motorbike import Motorbike
from garage.Vehicle import Vehicle


class TestMotorbike(unittest.TestCase):

    def setUp(self):
        """
        Set up a Motorbike instance for testing.
        """
        self.motorbike = Motorbike(id=1, brand="Yamaha", model="R1", year=2020, color="Blue", mot=True,
                                   fuel_level=100.0)

    def test_initialization(self):
        """
        Test if the Motorbike object is initialized correctly.
        """
        self.assertEqual(self.motorbike.brand, "Yamaha")
        self.assertEqual(self.motorbike.model, "R1")
        self.assertEqual(self.motorbike.year, 2020)
        self.assertEqual(self.motorbike.color, "Blue")
        self.assertEqual(self.motorbike.mot, True)
        self.assertEqual(self.motorbike.fuel_level, 100.0)

    def test_setters_and_getters(self):
        """
        Test the setters and getters for attributes.
        """
        self.motorbike.brand = "Honda"
        self.motorbike.model = "CBR"
        self.motorbike.year = 2022
        self.motorbike.color = "Red"

        self.assertEqual(self.motorbike.brand, "Honda")
        self.assertEqual(self.motorbike.model, "CBR")
        self.assertEqual(self.motorbike.year, 2022)
        self.assertEqual(self.motorbike.color, "Red")

    def test_str_method(self):
        """
        Test the __str__ method for correct string formatting.
        """
        expected_str = "Motorbike - 2020 Yamaha R1 (Blue), MOT Status: Operational, Fuel Level: 100.0%"
        self.assertEqual(str(self.motorbike), expected_str)

    def test_inheritance(self):
        """
        Test if Motorbike inherits from Vehicle correctly.
        """
        self.assertTrue(issubclass(Motorbike, Vehicle))

    def test_motorbike_with_zero_fuel(self):
        """
        Test if the Motorbike can be created with zero fuel.
        """
        motorbike_zero_fuel = Motorbike(id=2, brand="Kawasaki", model="Ninja", year=2021, color="Green", mot=True,
                                        fuel_level=0.0)
        self.assertEqual(motorbike_zero_fuel.fuel_level, 0.0)

    def test_mot_status(self):
        """
        Test if the MOT status is correctly set and reported.
        """
        motorbike_no_mot = Motorbike(id=3, brand="Suzuki", model="Hayabusa", year=2021, color="Black", mot=False)
        self.assertFalse(motorbike_no_mot.mot)


# To run the tests
if __name__ == "__main__":
    unittest.main()
