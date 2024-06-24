# client.py

class Client:
    def __init__(self, name, id, age, match_tickets=[]):
        self.name = name
        self.id = id
        self.age = age
        self.match_ticket = match_tickets
        self.total_tickets_general = 0
        self.total_tickets_vip = 0
        self.total_tickets = 0

    def __str__(self):
        return f"Nombre: {self.name}, ID: {self.id}, Edad: {self.age} {"Boleto: " + self.match_ticket if self.match_ticket else 'sin boleto'}"
    
