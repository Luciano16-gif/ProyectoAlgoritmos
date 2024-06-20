# App.py

#import sys
#import os

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gestionDePartidosyEstadios.MatchInfo import MatchInfo
from gestionDePartidosyEstadios.stadium import Stadium
from gestionDePartidosyEstadios.teams import Teams

class App:
    def __init__(self, data) -> None:
        """
        Initializes a new instance of the App class.

        Args:
            data (dict): La data que contiene el JSON.

        Returns:
            None
        """
        self.data = data
        self.teams = []
        self.stadiums = []
        self.matches = []
        self.register_data()

    def register_data(self):
        """
        Registers the data by calling the `register_teams`, `register_stadiums`, and `register_matches` methods.

        This method initializes the `teams`, `stadiums`, and `matches` attributes of the `App` instance by calling the respective registration methods.

        Parameters:
            self (App): The current instance of the `App` class.

        Returns:
            None
        """
        self.register_teams()
        self.register_stadiums()
        self.register_matches()

    def register_teams(self):
        """
        Registers the teams by iterating over the teams data and appending Teams instances to the teams list.

        Args:
            self: The App instance.
        
        Returns:
            None
        """
        for team in self.data['teams']:
            self.teams.append(Teams(team['id'], team['name'], team['code'], team['group']))

    def register_stadiums(self):
        """
        Registers the stadiums by iterating over the stadiums data and appending Stadium instances to the stadium list.

        This method takes no parameters.

        Returns:
            None
        """
        for stadium in self.data['stadiums']:
            self.stadiums.append(Stadium(stadium['id'],stadium['name'], stadium['city']))

    def register_matches(self):
        """
        Iterates over the matches data and appends MatchInfo instances to the matches list.

        This method initializes the matches attribute of the App instance by creating MatchInfo instances based on the local and visitor teams, match time, and stadium.

        Parameters:
            self: The App instance.

        Returns:
            None
        """
        for match in self.data['matches']:
            local_team = next((team for team in self.teams if team.fifa_code == match['home']['code']), None) 
            # next() found in the official Python documentation
            # It returns the next item from the iterator or None if no item is found.
            visitor_team = next((team for team in self.teams if team.fifa_code == match['away']['code']), None)
            stadium = next((stadium for stadium in self.stadiums if stadium.id == match['stadium_id']), None)
            self.matches.append(MatchInfo(match['id'], local_team, visitor_team, match['date'], stadium))

    def search_team_name_matches(self, name):
        """
        Searches for matches in the matches list that match the provided name.

        Args:
            name (str): The name of the name to search for.

        Returns:
            list: A list of MatchInfo objects that match the name.
        """

        matches = [match for match in self.matches if match.local_team.name == name or match.visitor_team.name == name]
        if not matches:
            print(f"No se han encontrado partidos para el equipo de {name}")
        return matches
    
    def search_stadium_matches(self, stadium):
        """
        Searches for matches in the matches list that match the provided stadium.

        Args:
            stadium (str): The name of the stadium to search for.

        Returns:
            list: A list of MatchInfo objects that match the stadium.
        """
        matches = [match for match in self.matches if match.stadium.name == stadium]
        if not matches:
            print(f"No se han encontrado partidos en el estadio {stadium}")
        return matches
    
    def search_date_matches(self, date):
        """
        Searches for matches in the matches list that match the provided date.

        Args:
            date (str): The date to search for.

        Returns:
            list: A list of MatchInfo objects that match the date.
        """
        matches = [match for match in self.matches if match.date == date]
        if not matches:
            print(f"No se han encontrado partidos para la fecha {date}")
        return matches




    def menu(self):
        while True:
            print("-----------------------------------------")
            print("Coloca el número de lo que quieres buscar: ")
            print("1. Buscar partidas por equipo")
            print("2. Buscar las partidas por estadio")
            print("3. Listar partidos por fecha")
            print("4. Salir")
            print("-----------------------------------------")

            try:
                option = int(input())
                if option == 1: # Listar equipos
                    try:
                        name = input("Coloca el nombre del equipo: ")
                        matches = self.search_team_name_matches(name)
                        print("-----------------------------------------------------------------")
                        for match in matches:
                            print(match)	
                    except ValueError:
                        print("Porfavor introduce un equipo valido")
                elif option == 2: # Listar estadios
                    try:
                        stadium = input("Coloca el nombre del estadio: ")
                        matches = self.search_stadium_matches(stadium)
                        print("-----------------------------------------------------------------")
                        for match in matches:
                            print(match)
                    except ValueError:
                        print("Porfavor introduce un equipo valido")
                elif option == 3: # Listar partidos
                    try:
                        date = input("Coloca la fecha del partido (yyyy-mm-dd): ")
                        matches = self.search_date_matches(date)
                        print("-----------------------------------------------------------------")
                        for match in matches:
                            print(match)
                    except ValueError:
                        print("Porfavor introduce un equipo valido")
                elif option == 4: # Salir
                    break
                else:
                    print("Porfavor selecciona una opción valida")
            except ValueError:
                print("Porfavor selecciona una opción valida")


