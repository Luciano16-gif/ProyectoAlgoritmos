#stadium.py

class Stadium:
    def __init__(self, name, location) -> None:
        """
        Initializes a new instance of the Stadium class.

        Args:
            name: The name of the stadium.
            location: The location of the stadium.

        Returns:
            None
        """
        self.name = name
        self.location = location
    
    def __str__(self) -> str:
        """
        Returns a string representation of the Stadium object.

        This method returns a formatted string that includes the name and location of the stadium.
        The string has the following format: "Stadio: {name}, Ubicación: {location}".

        Returns:
            str: The string representation of the Stadium object.
        """
        return f"Stadio: {self.name}, Ubicación: {self.location}"