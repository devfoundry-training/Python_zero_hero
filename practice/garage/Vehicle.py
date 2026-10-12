class Vehicle:
    """
    A class representing a vehicle with operations like start, stop, status, and fuel management.
    """

    def __init__(self, id: int, mot: bool, fuel_level: float = 100.0):
        """
        Initializes the Vehicle object with operational state (MOT) and a given fuel level.

        Args:
            id (int): Unique identifier for the vehicle.
            mot (bool): Indicates whether the vehicle is operational.
            fuel_level (float): Initial fuel level (default is 100.0%).
        """
        self.id = id
        self._mot = mot
        self._fuel_level = max(0.0, min(fuel_level, 100.0))  # Ensure fuel level is between 0-100%
        self._is_running = self._mot and self._fuel_level > 0  # Ensures proper state

    @property
    def fuel_level(self):
        """Gets the current fuel level."""
        return self._fuel_level

    @fuel_level.setter
    def fuel_level(self, value):
        """Sets the fuel level while ensuring it's between 0-100%."""
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("Fuel level must be a non-negative number.")
        self._fuel_level = min(value, 100.0)
        self._update_running_status()

    @property
    def mot(self):
        """Gets the MOT status (True if operational, False otherwise)."""
        return self._mot

    @mot.setter
    def mot(self, value):
        """Sets the MOT status and updates running status."""
        if not isinstance(value, bool):
            raise ValueError("MOT status must be a boolean value.")
        self._mot = value
        self._update_running_status()

    @property
    def is_running(self):
        """Gets the running status of the vehicle."""
        return self._is_running

    def _update_running_status(self):
        """Updates the running status based on MOT and fuel level."""
        self._is_running = self._mot and self._fuel_level > 0

    def start(self):
        """
        Starts the vehicle if it is operational (MOT is valid) and has fuel.
        """
        if not self._mot:
            print("Cannot start the vehicle. It is not operational (MOT expired).")
            return

        if self._fuel_level <= 0:
            print("Cannot start the vehicle. No fuel.")
            return

        if not self._is_running:
            self._is_running = True
            print("The vehicle has started.")
        else:
            print("The vehicle is already running.")

    def stop(self):
        """
        Stops the vehicle by setting the operational state to not running.
        """
        if self._is_running:
            self._is_running = False
            print("The vehicle has stopped.")
        else:
            print("The vehicle is already stopped.")

    def refuel(self, amount: float):
        """
        Refuels the vehicle by a given amount, ensuring fuel level doesn't exceed 100%.

        Args:
            amount (float): The amount of fuel to add (must be positive).
        """
        if amount < 0:
            print("Invalid fuel amount. Cannot be negative.")
            return

        self.fuel_level = self._fuel_level + amount  # Uses the setter, which ensures max 100%
        print(f"Vehicle refueled. Current fuel level: {self._fuel_level:.1f}%")

    def check_fuel(self):
        """
        Returns the current fuel level of the vehicle.

        Returns:
            float: The current fuel level as a percentage.
        """
        return self._fuel_level

    def __str__(self) -> str:
        """
        Provides a string representation of the Vehicle object, showing its operational status and fuel level.

        Returns:
            str: A formatted string with the vehicle's MOT status and fuel level.
        """
        return f"Vehicle - MOT Status: {'Operational' if self._mot else 'Not Operational'}, Fuel Level: {self._fuel_level:.1f}%"

    def display_status(self):
        """
        Displays the current status of the vehicle (running or not running) and the fuel level.
        """
        running_status = "Running" if self._is_running else "Not Running"
        return f"The vehicle is {running_status}. Current fuel level: {self._fuel_level:.1f}%"

    def check_mot(self):
        """
        Checks if the vehicle is operational.

        Returns:
            bool: Whether the vehicle is operational.
        """
        return self._mot

    def update_mot(self, status: bool):
        """
        Updates the operational status of the vehicle (MOT status).

        Args:
            status (bool): The new MOT status. True for operational, False for not operational.
        """
        self.mot = status  # Uses the setter to ensure consistency
        print(f"Vehicle MOT updated. Now it is {'operational' if self._mot else 'not operational'}.")
