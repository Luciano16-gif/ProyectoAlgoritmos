from gestionDeClientes.client import Client
from gestionDeClientes.ticket import Ticket
from funcionalidad.getUserInput import get_user_input, name_model, is_alpha, id_check, age_limit, is_in_options

def create_client():
        """
        Creates a new client object by prompting the user for their name, ID, and age.

        Returns:
            - A new Client object with the provided name, ID, and age.
            - 'M' if the user enters 'menu' to return to the menu.

        Raises:
            - None

        Notes:
            - This function uses the get_user_input function to prompt the user for their name, ID, and age.
            - The name is validated using the is_alpha validator function.
            - The ID is validated using the id_check validator function.
            - The age is validated using the age_limit validator function.
        """
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
    option = get_user_input("", int, lambda x: is_in_options(x, [1, 2]))
    # Lambda functions are small anonymous functions defined with the lambda keyword. 
    # They can have any number of arguments, but only one expression. The expression is evaluated and returned.
    # Lambda was taken from the official Python documentation.
    if option == 1:
        ticket_type = "General"
        price = 35
    else:
        ticket_type = "VIP"
        price = 75
    return ticket_type, price




