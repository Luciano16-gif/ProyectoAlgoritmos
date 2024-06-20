from gestionDeClientes.client import Client

class Ticket:
    def __init__(self, cliente, partido, tipo_entrada, asiento):
        self.cliente = cliente
        self.partido = partido
        self.tipo_entrada = tipo_entrada
        self.asiento = asiento
        self.codigo = f"{cliente.cedula}"
