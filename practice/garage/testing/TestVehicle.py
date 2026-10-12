import unittest

from garage.Vehicle import Vehicle


class TestVehicle(unittest.TestCase):

    def setUp(self):
        """
        Set up a Vehicle instance for testing.
        """
        self.vehicle = Vehicle(id=1, mot=True, fuel_level=50.0)

    def test_initialization(self):
        """
        Test if the Vehicle object is initialized correctly.
        """
        self.assertEqual(self.vehicle.id, 1)
        self.assertEqual(self.vehicle.mot, True)
        self.assertEqual(self.vehicle.fuel_level, 50.0)
        self.assertEqual(self.vehicle.is_running, True)

    def test_start(self):
        """
        Test the start method.
        """
        self.vehicle.start()
        self.assertTrue(self.vehicle.is_running)
        self.vehicle.start()  # Test starting again
        self.assertTrue(self.vehicle.is_running)

    def test_start_with_no_fuel(self):
        """
        Test that the vehicle cannot start when there's no fuel.
        """
        self.vehicle.fuel_level = 0
        self.vehicle.start()
        self.assertFalse(self.vehicle.is_running)

    def test_stop(self):
        """
        Test the stop method.
        """
        self.vehicle.stop()
        self.assertFalse(self.vehicle.is_running)
        self.vehicle.stop()  # Test stopping again
        self.assertFalse(self.vehicle.is_running)

    def test_refuel(self):
        """
        Test the refuel method to ensure fuel is added correctly.
        """
        self.vehicle.refuel(20)  # Refuel by 20%
        self.assertEqual(self.vehicle.fuel_level, 70.0)

    def test_refuel_over_100(self):
        """
        Test refueling beyond 100%. It should not exceed 100%.
        """
        self.vehicle.refuel(60)  # Refuel by 60%, which should cap at 100%
        self.assertEqual(self.vehicle.fuel_level, 100.0)

    def test_invalid_refuel(self):
        """
        Test refueling with a negative amount.
        """
        self.vehicle.refuel(-10)  # Invalid fuel amount
        self.assertEqual(self.vehicle.fuel_level, 50.0)  # Should not change

    def test_check_fuel(self):
        """
        Test the check_fuel method.
        """
        self.assertEqual(self.vehicle.check_fuel(), 50.0)

    def test_display_status(self):
        """
        Test the display_status method.
        """
        self.assertEqual(self.vehicle.display_status(), "The vehicle is Running. Current fuel level: 50.0%")
        self.vehicle.stop()
        self.assertEqual(self.vehicle.display_status(), "The vehicle is Not Running. Current fuel level: 50.0%")

    def test_check_mot(self):
        """
        Test the check_mot method.
        """
        self.assertTrue(self.vehicle.check_mot())
        self.vehicle.update_mot(False)
        self.assertFalse(self.vehicle.check_mot())

    def test_update_mot(self):
        """
        Test the update_mot method to change the MOT status.
        """
        self.vehicle.update_mot(False)
        self.assertFalse(self.vehicle.mot)
        self.assertFalse(self.vehicle.is_running)

    def test_str_method(self):
        """
        Test the __str__ method for correct string formatting.
        """
        expected_str = "Vehicle - MOT Status: Operational, Fuel Level: 50.0%"
        self.assertEqual(str(self.vehicle), expected_str)

    def test_vehicle_not_operational(self):
        """
        Test if a non-operational vehicle behaves correctly.
        """
        non_operational_vehicle = Vehicle(id=2, mot=False, fuel_level=50.0)
        self.assertFalse(non_operational_vehicle.is_running)

        non_operational_vehicle.start()
        self.assertFalse(non_operational_vehicle.is_running)


# To run the tests
if __name__ == "__main__":
    unittest.main()
