# client.py

class Client:
    def __init__(self, name, id, age, match_ticket=None):
        self.name = name
        self.id = id
        self.age = age

    def show(self):
        return f"Nombre: {self.name}, ID: {self.id}, Edad: {self.age} {"Botelto: " + self.match_ticket if self.match_ticket else 'sin boleto'}"