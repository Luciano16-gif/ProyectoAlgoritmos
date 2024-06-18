# teams.py

class Teams:
    def __init__(self, country, fifa_code, group):
        """
        Initializes a new instance of the Teams class.

        Args:
            country (str): The name of the country.
            fifa_code (str): The FIFA code of the country.
            group (str): The group of the country.

        Returns:
            None
        """
        self.country = country
        self.fifa_code = fifa_code
        self.group = group

    def __str__(self):
        return f"País: {self.country}, Código FIFA: {self.fifa_code}, Grupo: {self.group}"