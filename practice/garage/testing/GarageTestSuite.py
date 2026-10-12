import unittest

from garage.testing.TestCar import TestCar
from garage.testing.TestMotorbike import TestMotorbike
from garage.testing.TestVehicle import TestVehicle


# Run this class from here, running it at the suite level will cause an empty suite issue.
class TestSuite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Called before any tests in the suite"""
        print("Setting up resources for the entire test suite...")
        # Initialize resources that are shared across test classes
        cls.global_resource = "Suite-level resource initialized"

    @classmethod
    def tearDownClass(cls):
        """Called after all tests in the suite"""
        print("Cleaning up resources for the entire test suite...")
        cls.global_resource = None

    @classmethod
    def suite(cls):
        suite = unittest.TestSuite()
        print("Adding TestVehicle to the suite...")
        suite.addTest(unittest.makeSuite(TestVehicle))
        print("Adding TestCar to the suite...")
        suite.addTest(unittest.makeSuite(TestCar))
        print("Adding TestMotorbike to the suite...")
        suite.addTest(unittest.makeSuite(TestMotorbike))
        return suite


# If you want to run the suite directly:
if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(TestSuite.suite())
