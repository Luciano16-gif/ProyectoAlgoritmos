# client.py

class Client:
    def __init__(self, name, id, age, match_ticket):
        self.name = name
        self.id = id
        self.age = age

    def __str__(self):
        return f"Nombre: {self.name}, ID: {self.id}, Edad: {self.age}"