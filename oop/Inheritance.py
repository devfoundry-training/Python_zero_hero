# ============================================================
# Inheritance - Base Classes, Overriding, Polymorphism
# ============================================================


class Animal:
    """Base class for all animals."""

    def __init__(self, name, species):
        self.name = name
        self.species = species

    def speak(self):
        """Abstract method to be implemented by subclasses."""
        raise NotImplementedError("Subclass must implement abstract method")

    def move(self):
        """General movement behavior for all animals."""
        print(f"{self.name} is moving.")

    def sleep(self):
        """General sleep behavior for all animals."""
        print(f"{self.name} is sleeping.")


class Dog(Animal):
    """Dog class, inheriting from Animal, with breed-specific behavior."""

    def __init__(self, name, breed):
        super().__init__(name, "Dog")
        self.breed = breed

    def speak(self):
        """Dog-specific implementation of speak method."""
        print(f"{self.name} says Woof!")

    def fetch(self):
        """Dog-specific behavior for fetching."""
        print(f"{self.name} is fetching the ball.")


class Cat(Animal):
    """Cat class, inheriting from Animal, with colour-specific behavior."""

    def __init__(self, name, colour):
        super().__init__(name, "Cat")
        self.colour = colour

    def speak(self):
        """Cat-specific implementation of speak method."""
        print(f"{self.name} says Meow!")

    def scratch(self):

        """Cat-specific behavior for scratching."""
        print(f"{self.name} is scratching the post.")
