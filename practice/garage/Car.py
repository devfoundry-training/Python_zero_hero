from garage.Vehicle import Vehicle


class Car(Vehicle):
    """
    A class representing a Car, inheriting from the Vehicle class.
    Includes specific attributes for a car like make, model, mileage, and year.
    """

    def __init__(self, id: int, make: str, model: str, mileage: int, year: int, mot: bool, fuel_level: float = 100.0):
        """
        Initializes the Car object with additional attributes (make, model, mileage, year) and MOT status.

        Args:
            make (str): The car's make (e.g., Toyota).
            model (str): The car's model (e.g., Corolla).
            mileage (int): The car's mileage (in kilometers).
            year (int): The year of manufacture of the car.
            mot (bool): Whether the car is operational or not.
            fuel_level (float): The initial fuel level of the vehicle (default is 100.0%).
        """
        super().__init__(id, mot, fuel_level)  # Initialize the parent class (Vehicle)
        self.__make = make
        self.__model = model
        self.__mileage = mileage
        self.__year = year

    @property
    def make(self):
        """
        Gets the make of the car.

        Returns:
            str: The car's make (e.g., Toyota).
        """
        return self.__make

    @make.setter
    def make(self, value: str):
        """
        Sets the make of the car.

        Args:
            value (str): The new make of the car (e.g., Honda).
        """
        self.__make = value

    @property
    def model(self):
        """
        Gets the model of the car.

        Returns:
            str: The car's model (e.g., Corolla).
        """
        return self.__model

    @model.setter
    def model(self, value: str):
        """
        Sets the model of the car.

        Args:
            value (str): The new model of the car (e.g., Civic).
        """
        self.__model = value

    @property
    def mileage(self):
        """
        Gets the mileage of the car.

        Returns:
            int: The car's mileage (in kilometers).
        """
        return self.__mileage

    @mileage.setter
    def mileage(self, value: int):
        """
        Sets the mileage of the car.

        Args:
            value (int): The new mileage of the car (in kilometers).
        """
        self.__mileage = value

    @property
    def year(self):
        """
        Gets the year of manufacture of the car.

        Returns:
            int: The year the car was manufactured.
        """
        return self.__year

    @year.setter
    def year(self, value: int):
        """
        Sets the year of manufacture of the car.

        Args:
            value (int): The new year of the car.
        """
        self.__year = value

    def __str__(self) -> str:
        """
        Provides a string representation of the Car object, showing make, model, mileage, and MOT status.

        Returns:
            str: A formatted string with the car's make, model, mileage, year, and MOT status.
        """
        return f'Make: {self.__make}, Model: {self.__model}, Mileage: {self.__mileage} km, Year: {self.__year}, MOT Status: {self.mot}'
