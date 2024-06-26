from gestionDeClientes.client import Client

class Ticket:
    def __init__(self, client, match, ticket_type, seat):
        self.client = client
        self.match = match
        self.ticket_type = ticket_type
        self.seat = seat
        self.code = client.id

    def __str__(self):
        return f"Código: {self.code}, Partido: {self.match.id}, Tipo de entrada: {self.ticket_type}, Asiento: {self.seat}"