# client.py

class Client:
    def __init__(self, name, id, age):
        self.name = name
        self.id = id
        self.age = age
        self.match_tickets = []
        self.total_tickets_general = 0
        self.total_tickets_vip = 0
        self.total_tickets = 0

    def __str__(self):
        tickets_str = "\n  ".join([str(ticket) for ticket in self.match_tickets])
        if not tickets_str:
            tickets_str = 'sin boleto'
        return f"Nombre: {self.name}, ID: {self.id}, Edad: {self.age}, Boletos: {tickets_str}"
    
