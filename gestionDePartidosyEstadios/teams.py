# teams.py

class Teams:
    def __init__(self, id, name, fifa_code, group):
        """
        Initializes a new instance of the Teams class.

        Args:
            name (str): The name of the name.
            fifa_code (str): The FIFA code of the name.
            group (str): The group of the name.

        Returns:
            None
        """
        self.id = id
        self.name = name
        self.fifa_code = fifa_code
        self.group = group

    def __str__(self):
        return f"Nombre: {self.name}, Código FIFA: {self.fifa_code}, Grupo: {self.group}"