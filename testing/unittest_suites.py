# ============================================================
# Test Suites - Grouping and Running Tests Together
# ============================================================
# Test suites let you bundle related test classes and run them
# as a single unit. Useful for organising tests by module or
# feature as the project grows.
# ============================================================

import unittest


class TestUser(unittest.TestCase):
    """Test class for User - placeholder for suite demonstration."""

    @classmethod
    def suite(cls):
        """Creates a test suite containing all tests in this class."""
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestUser))
        return suite


if __name__ == "__main__":
    unittest.TextTestRunner().run(TestUser.suite())
