# ============================================================
# unittest - Test Classes, Assertions, Setup/Teardown
# ============================================================


class User:
    """A class representing a User."""

    def __init__(self, username, email, age):
        """
        Initializes the User object with username, email, and age.

        >>> user = User('john_doe', 'john@example.com', 30)
        >>> user.username
        'john_doe'
        >>> user.email
        'john@example.com'
        >>> user.age
        30
        """
        self.username = username
        self.email = email
        self.age = age

    def update_email(self, new_email):
        """
        Updates the user's email address.

        >>> user = User('john_doe', 'john@example.com', 30)
        >>> user.update_email('john_new@example.com')
        >>> user.email
        'john_new@example.com'
        """
        self.email = new_email

    def update_age(self, new_age):
        """
        Updates the user's age.

        >>> user = User('john_doe', 'john@example.com', 30)
        >>> user.update_age(31)
        >>> user.age
        31
        """
        self.age = new_age

    def __str__(self):
        """
        Returns a string representation of the User object.

        >>> user = User('john_doe', 'john@example.com', 30)
        >>> str(user)
        'User: john_doe, Email: john@example.com, Age: 30'
        """
        return f"User: {self.username}, Email: {self.email}, Age: {self.age}"


# Unittest for User Class
import unittest


class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Runs once before all test methods."""
        print("Before class: Running once before all tests")

    @classmethod
    def tearDownClass(cls):
        """Runs once after all test methods."""
        print("After class: Running once after all tests")

    def setUp(self) -> None:
        """Runs before every test method."""
        print("Before method: Running before each test method")
        self.user = User('john_doe', 'john@example.com', 30)

    def tearDown(self) -> None:
        """Runs after every test method."""
        print("After method: Running after each test method")

    def test_init(self):
        """Test initialization of User object."""
        self.assertEqual(self.user.username, 'john_doe')
        self.assertEqual(self.user.email, 'john@example.com')
        self.assertEqual(self.user.age, 30)

    def test_update_email(self):
        """Test updating email of User object."""
        self.user.update_email('john_new@example.com')
        self.assertEqual(self.user.email, 'john_new@example.com')

    def test_update_age(self):
        """Test updating age of User object."""
        self.user.update_age(31)
        self.assertEqual(self.user.age, 31)

    def test_str_method(self):
        """Test string representation of User object."""
        expected_str = 'User: john_doe, Email: john@example.com, Age: 30'
        self.assertEqual(str(self.user), expected_str)


# To run the tests
if __name__ == "__main__":
    # Running doctests
    import doctest

    doctest.testmod()

    # Running unittest
    unittest.main()
