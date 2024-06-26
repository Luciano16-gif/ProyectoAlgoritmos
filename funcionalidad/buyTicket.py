from gestionDeClientes.client import Client
from gestionDeClientes.ticket import Ticket

def get_user_input(prompt, input_type=str, validator=None):
    while True:
        user_input = input(prompt)
        if user_input.lower() == 'menu':
            return 'M'
        try:
            user_input = input_type(user_input)
            if validator and not validator(user_input):
                raise ValueError
            return user_input
        except ValueError:
            print("Por favor, introduce un valor válido.")

def is_alpha(string):
    """
    Check if a given string consists only of alphabetic characters.

    Args:
        string (str): The string to be checked.

    Returns:
        bool: True if the string consists only of alphabetic characters, False otherwise.
    """

    return string.isalpha()

def age_limit(age):
    """
    Check if the given age is within the valid range of 0 to 130.

    Args:
        age (int): The age to be checked.

    Returns:
        bool: True if the age is within the valid range, False otherwise.
    """
    if age < 0 or age > 130:
        print("Porfavor introduce una edad entre 0 y 130")
        return False
    return True

def id_check(id):
    """
    Check if the given ID is within the valid range of 1 to 2000000000.

    Args:
        id (int): The ID to be checked.

    Returns:
        bool: True if the ID is within the valid range, False otherwise.
    """
    if id < 1 or id > 2000000000:
        print("Porfavor introduce un ID entre 1 y 2000000000")
        return False
    return True

def name_model(name):
    name = name.lower()
    name = name[0].upper() + name[1:]


def create_client():
        print("Por favor ingresa tus datos (o ingresa 'menu' para volver al menú)")
        name = get_user_input("Ingresa tu nombre: ", str, validator=is_alpha)
        if name == 'M':
            return 'M'
        name = name_model(name)
        id = get_user_input("Ingresa tu número de cédula: ", int, validator=id_check)
        if id == 'M':
            return 'M'
        age = get_user_input("Ingresa tu edad: ", int, validator=age_limit)
        if age == 'M':
            return 'M'
        return Client(name, id, age)

def type_ticket():
    """
    A function that prompts the user to select a ticket type between General and VIP.
    If the user enters an invalid option, it prompts for a valid choice.
    Returns a tuple containing the selected ticket type (General or VIP) and its corresponding price.
    """
    print("Coloque el número del tipo de boleto que desea comprar: \n1. General\n2. Vip\n")
    while True:
        try:
            option = int(input())
            if option not in [1, 2]:
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


