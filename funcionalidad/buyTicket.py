from gestionDeClientes.client import Client
from gestionDeClientes.ticket import Ticket

def create_client():
    while True:
        try:
            print("Porfavor ingresa tus datos")
            name = input("Ingresa tu nombre: ")
            id = int(input("Ingresa tu numero de cedula: "))
            age = int(input("Ingresa tu edad: "))
            return Client(name, id, age)
        except ValueError:
            print("Porfavor introduce un valor válido") 

def type_ticket():
    print("Coloque el número del tipo de boleto que desea comprar: \n1. General\n2. Vip\n")
    while True:
        try:
            option = int(input())
            if option != 1 and option != 2:
                print("Porfavor introduce un valor entre 1 y 2")
            else:
                break
        except ValueError:
            print("Porfavor introduce un valor numerico")
    if option == 1:
        ticket_type = "General"
        price = 35
    else:
        ticket_type = "VIP"
        price = 75
    return ticket_type, price

def vampire_number(id):
        
        if id < 1260:  # The smallest vampire number is 1260
            return False
    
        str_id = str(id)
        len_id = len(str_id)
    
        if len_id % 2 != 0:  # Must have an even number of digits
            return False
    
        half_len = len_id // 2
    
        # Iterate over potential fangs
        for x in range(10**(half_len - 1), 10**half_len):
            if id % x == 0:
                y = id // x
                # Ensure y has the correct number of digits
                if 10**(half_len - 1) <= y < 10**half_len:
                    # Check if neither x nor y end in 0
                    if not (x % 10 == 0 and y % 10 == 0):
                        # Check if the digits of x and y match the digits of n
                        if sorted(str(x) + str(y)) == sorted(str_id):
                            return True
    
        return False
