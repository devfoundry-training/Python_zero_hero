import unittest

from calculator.Calculator import Calculator


class TestCalculator(unittest.TestCase):
    # Before All - Runs once before all cases
    @classmethod
    def setUpClass(cls):
        print("set up calculator")
        cls.shared_resource = "Calculator is ready to go!"

    # Before Each Test - Runs for each testcase

    def setUp(self) -> None:
        self.my_calculator = Calculator(5, 3)

    def test_init(self):
        self.assertTrue(isinstance(self.my_calculator, Calculator), True)

    def test_addition(self):
        self.assertEqual(self.my_calculator.addition(), 8)

    def test_subtraction(self):
        self.assertEqual(self.my_calculator.subtraction(), 2)

    def test_multiplication(self):
        self.assertEqual(self.my_calculator.multiplication(), 15)

    def test_division(self):
        self.assertAlmostEqual(self.my_calculator.division(), 1.6666, delta=0.0001)

    def test_division_by_zero(self):
        self.my_calc = Calculator(1, 0)
        self.assertEqual(self.my_calc.division(), "Error: Cannot divide by zero.")

    # After Each Test - Runs for each testcase
    def tearDown(self) -> None:
        print("Tearing down after a test case...")
        self.my_calculator = None

    # After All - Runs at the end (once)
    @classmethod
    def tearDownClass(cls):
        print("cleaning up calculator")
        cls.shared_resource = None
