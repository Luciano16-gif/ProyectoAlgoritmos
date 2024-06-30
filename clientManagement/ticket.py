# ticket.py

class Ticket:
    def __init__(self, client, match, ticket_type, seat, code = None, used = False):
        """
        Initializes a Ticket object with the provided client, match, ticket type, seat, code, and used status.

        Parameters:
            client: Client object representing the ticket owner.
            match: Match object representing the match associated with the ticket.
            ticket_type: String indicating the type of ticket.
            seat: String indicating the seat number.
            code: String representing the ticket code. If not provided, it is generated.
            used: Boolean indicating if the ticket has been used.

        Returns:
            None
        """
        self.client = client
        self.match = match
        self.ticket_type = ticket_type
        self.seat = seat
        self.code = code if code is not None else self.generate_ticket_code()
        self.used = used

    def generate_ticket_code(self):
        """
        Generate a unique ticket code using the client's ID and the seat number
        hash() returns the hash value of the object (in this case, a tuple). Taken from the official Python documentation.
        https://docs.python.org/3/library/functions.html#hash
        """
        # Generate a unique ticket code 
        return hash((self.client.id, self.seat))

    def __str__(self):
        """
        A method to return a formatted string representing the ticket information including code, match details, ticket type, and seat number.
        """
        return f"Código: {self.code}, Partido: {self.match.local_team.name} vs {self.match.visitor_team.name}, Tipo de entrada: {self.ticket_type}, Asiento: {self.seat}"