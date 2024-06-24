# MatchInfo.py

class MatchInfo:
    def __init__(self, id, local_team, visitor_team, date, stadium) -> None:
        """
        Initializes a new instance of the MatchInfo class.
    
        Args:
            local_team (Teams): The local team.
            visitor_team (Teams): The visiting team.
            date (str): The date of the match.
            stadium (Stadium): The stadium where the match is being played.

        Returns:
            None
        """
        self.id = id
        self.local_team = local_team
        self.visitor_team = visitor_team
        self.date = date
        self.stadium = stadium  
        self.tickets = []

    def __str__(self) -> str:
        return f"{self.local_team.name} (Local) vs, Visitante: {self.visitor_team.name}, Hora: {self.date}, Estadio: {self.stadium.name}, {self.stadium.location}\nId del partido: {self.id}"
