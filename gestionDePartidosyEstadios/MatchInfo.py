# MatchInfo.py

class MatchInfo:
    def __init__(self, local_team, visitor_team, time, stadium) -> None:
        """
        Initializes a new instance of the MatchInfo class.
    
        Args:
            local_team (Teams): The local team.
            visitor_team (Teams): The visiting team.
            time (str): The time of the match.
            stadium (Stadium): The stadium where the match is being played.

        Returns:
            None
        """
        self.local_team = local_team
        self.visitor_team = visitor_team
        self.time = time
        self.stadium = stadium  

    def __str__(self) -> str:
        return f"Local: {self.local_team}, Visitante: {self.visitor_team}, Hora: {self.time}, Estadio: {self.stadium}"
