# App.py

from MatchInfo import MatchInfo
from stadium import Stadium
from teams import Teams

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
            self.teams.append(Teams(team['country'], team['fifa_code'], team['group']))

    def register_stadiums(self):
        """
        Registers the stadiums by iterating over the stadiums data and appending Stadium instances to the stadium list.

        This method takes no parameters.

        Returns:
            None
        """
        for stadium in self.data['stadiums']:
            self.stadiums.append(Stadium(stadium['name'], stadium['location']))

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
            local_team = next((team for team in self.teams if team.fifa_code == match['local_team']), None)
            visitor_team = next((team for team in self.teams if team.fifa_code == match['visitor_team']), None)
            stadium = next((stadium for stadium in self.stadiums if stadium.name == match['stadium']), None)
            self.matches.append(MatchInfo(local_team, visitor_team, match['time'], stadium))



