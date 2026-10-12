# ============================================================
# Further Abstraction - Properties, Class Methods, Static Methods
# ============================================================
# @abstractmethod - must be implemented by concrete subclasses
# @property      - can combine with @abstractmethod for abstract properties
# @classmethod   - operates on the class, not instances
# @staticmethod  - not tied to instance or class, used for organisation
# ============================================================

from abc import ABC, abstractmethod


class Animal(ABC):
    """Abstract base class for animals, enforcing essential behaviors."""

    def __init__(self, name):
        self.name = name

    @property
    @abstractmethod
    def species(self):
        """Abstract property to be defined by subclasses."""
        pass

    @abstractmethod
    def speak(self):
        """Abstract method to be implemented by subclasses."""
        pass

    def move(self):
        """Concrete method: Defines general movement behavior."""
        print(f"{self.name} is moving.")

    def sleep(self):
        """Concrete method: Defines general sleeping behavior."""
        print(f"{self.name} is sleeping.")

    @classmethod
    def animal_info(cls):
        """Class method: Provides general info about animals."""
        return "Animals are living beings that exhibit movement and behavior."

    @staticmethod
    def kingdom():
        """Static method: Returns the biological kingdom of animals."""
        return "Animalia"


class Dog(Animal):
    """Dog class, inheriting from Animal, with breed-specific behavior."""

    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed

    @property
    def species(self):
        """Defines the species property for Dog."""
        return "Dog"

    def speak(self):
        """Dog-specific implementation of speak method."""
        print(f"{self.name} says Woof!")

    def fetch(self):
        """Dog-specific behavior for fetching."""
        print(f"{self.name} is fetching the ball.")


class Cat(Animal):
    """Cat class, inheriting from Animal, with color-specific behavior."""

    def __init__(self, name, color):
        super().__init__(name)
        self.color = color

    @property
    def species(self):
        """Defines the species property for Cat."""
        return "Cat"

    def speak(self):
        """Cat-specific implementation of speak method."""
        print(f"{self.name} says Meow!")

    def scratch(self):
        """Cat-specific behavior for scratching."""
        print(f"{self.name} is scratching the post.")


class Bird(Animal):
    """Bird class, demonstrating additional behavior like flying."""

    def __init__(self, name, wing_span):
        super().__init__(name)
        self.wing_span = wing_span

    @property
    def species(self):
        """Defines the species property for Bird."""
        return "Bird"

    def speak(self):
        """Bird-specific implementation of speak method."""
        print(f"{self.name} chirps melodiously.")

    def fly(self):
        """Bird-specific method for flying."""
        print(f"{self.name} is flying with a wingspan of {self.wing_span} meters.")

