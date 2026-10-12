from garage.Vehicle import Vehicle


class Motorbike(Vehicle):
    """
    A class representing a motorbike, inheriting from the Vehicle class.
    """

    def __init__(self, id: int, brand: str, model: str, year: int, color: str, mot: bool, fuel_level: float = 100.0):
        """
        Initializes the Motorbike object with brand, model, year, color, MOT status, and fuel level.

        Args:
            brand (str): The brand of the motorbike (e.g., Yamaha, Harley-Davidson).
            model (str): The model of the motorbike (e.g., R1, Sportster).
            year (int): The manufacturing year of the motorbike.
            color (str): The color of the motorbike (e.g., Red, Black).
            mot (bool): Whether the motorbike is operational (MOT passed).
            fuel_level (float): The initial fuel level of the motorbike (default is 100.0%).
        """
        super().__init__(id, mot, fuel_level)
        self.__brand = brand
        self.__model = model
        self.__year = year
        self.__color = color

    @property
    def brand(self):
        """
        Gets the brand of the motorbike.

        Returns:
            str: The brand of the motorbike.
        """
        return self.__brand

    @brand.setter
    def brand(self, value: str):
        """
        Sets the brand of the motorbike.

        Args:
            value (str): The new brand of the motorbike.
        """
        self.__brand = value

    @property
    def model(self):
        """
        Gets the model of the motorbike.

        Returns:
            str: The model of the motorbike.
        """
        return self.__model

    @model.setter
    def model(self, value: str):
        """
        Sets the model of the motorbike.

        Args:
            value (str): The new model of the motorbike.
        """
        self.__model = value

    @property
    def year(self):
        """
        Gets the year of the motorbike.

        Returns:
            int: The manufacturing year of the motorbike.
        """
        return self.__year

    @year.setter
    def year(self, value: int):
        """
        Sets the year of the motorbike.

        Args:
            value (int): The new manufacturing year of the motorbike.
        """
        self.__year = value

    @property
    def color(self):
        """
        Gets the color of the motorbike.

        Returns:
            str: The color of the motorbike.
        """
        return self.__color

    @color.setter
    def color(self, value: str):
        """
        Sets the color of the motorbike.

        Args:
            value (str): The new color of the motorbike.
        """
        self.__color = value

    def __str__(self) -> str:
        """
        Provides a string representation of the Motorbike object, showing brand, model, year, color, and MOT status.

        Returns:
            str: A formatted string with the motorbike's brand, model, year, color, and operational status.
        """
        return f"Motorbike - {self.year} {self.brand} {self.model} ({self.color}), MOT Status: {'Operational' if self.mot else 'Not Operational'}, Fuel Level: {self.fuel_level:.1f}%"
