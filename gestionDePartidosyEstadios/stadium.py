#stadium.py

class Stadium:
    def __init__(self, id, name, location, capacity_general, capacity_vip) -> None:
        """
        Initializes a new instance of the Stadium class.

        Args:
            name: The name of the stadium.
            location: The location of the stadium.

        Returns:
            None
        """
        self.id = id
        self.name = name
        self.location = location
        self.capacity_general = capacity_general
        self.capacity_vip = capacity_vip
        self.taken_vip_seats = [1]
        self.taken_general_seats = [1]
    
    def __str__(self) -> str:
        """
        Returns a string representation of the Stadium object.

        This method returns a formatted string that includes the name and location of the stadium.
        The string has the following format: "Stadio: {name}, Ubicación: {location}".

        Returns:
            str: The string representation of the Stadium object.
        """
        return f"Stadio: {self.name}, Ubicación: {self.location}"