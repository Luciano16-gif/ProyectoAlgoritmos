# app.py

from gestionDePartidosyEstadios.MatchInfo import MatchInfo
from gestionDePartidosyEstadios.stadium import Stadium
from gestionDePartidosyEstadios.teams import Teams
from gestionDeClientes.ticket import Ticket
from funcionalidad.buyTicket import create_client, type_ticket
from funcionalidad.getUserInput import is_alpha, get_user_input, is_in_options
from funcionalidad.specialNumbers import vampire_number
from funcionalidad.storedData import Stored_Data
from funcionalidad.restaurantMenu import restaurant_menu
from funcionalidad.statisticsFolder.staticticsCode import write_statistics_to_file
import json

loaded_data = Stored_Data()



class App:
    def __init__(self, data) -> None:
        """
        Initializes a new instance of the App class.

        Args:
            data (dict): the data that contains the JSON.

        Returns:
            None
        """

        self.data = data
        self.teams = []
        self.stadiums = []
        self.matches = []
        self.clients = []
        self.products_for_storing = []
        self.products = []
        self.register_data()

    def register_data(self):
        """
        Registers the data by calling the `register_teams`, `register_stadiums`, and `register_matches` methods.

        This method initializes the `teams`, `stadiums`, and `matches` attributes of the `App` instance by calling the respective registration methods.

        Parameters:
            self (App): The current instance of the `App` class.

        Returns:
            None
        """

        self.register_teams()
        self.register_stadiums()
        self.register_matches()
        self.register_clients()
        self.register_tickets()
        self.update_products()
        self.store_data()

    def register_teams(self):
        """
        Registers the teams by iterating over the teams data and appending Teams instances to the teams list.

        Args:
            self: The App instance.
        
        Returns:
            None
        """
        for team in self.data['teams']:
            self.teams.append(Teams(team['id'], team['name'], team['code'], team['group']))

    def register_stadiums(self):
        """
        Registers the stadiums by iterating over the stadiums data and appending Stadium instances to the stadium list.

        This method takes no parameters.

        Returns:
            None
        """
        for stadium in self.data['stadiums']:
            self.stadiums.append(Stadium(stadium['id'],stadium['name'], stadium['city'], stadium['capacity'][0], stadium['capacity'][1], stadium['restaurants']))

        
    def register_matches(self):
        """
        Iterates over the matches data and appends MatchInfo instances to the matches list.

        This method initializes the matches attribute of the App instance by creating MatchInfo instances based on the local and visitor teams, match time, and stadium.

        Parameters:
            self: The App instance.

        Returns:
            None
        """
        
        for match in self.data['matches']:
            local_team = next((team for team in self.teams if team.fifa_code == match['home']['code']), None) 
            # next() found in the official Python documentation
            # It returns the next item from the iterator or None if no item is found.
            visitor_team = next((team for team in self.teams if team.fifa_code == match['away']['code']), None)
            stadium = next((stadium for stadium in self.stadiums if stadium.id == match['stadium_id']), None)
            self.matches.append(MatchInfo(match['id'], local_team, visitor_team, match['date'], stadium))

    def register_clients(self):
        """
        Registers the clients by assigning the `clients` attribute of the `App` instance with the `clients` attribute of the `loaded_data` object.

        This function does not take any parameters.

        Returns:
            None
        """
        self.clients = loaded_data.clients

    def register_tickets(self):
        """
        Registers tickets by iterating through the `loaded_data.tickets` list and creating `Ticket` objects for each ticket.

        This function assigns the `client` and `match` variables by searching for the client and match with the corresponding IDs in the `self.clients` and 
        `self.matches` lists. If a client and match are found, a `Ticket` object is created with the provided ticket information.

        The ticket object is then appended to the `match.tickets` list and the `client.match_tickets` list. The `client.total_tickets` and `match.used_tickets` 
        lists are also updated accordingly.

        If the ticket type is 'VIP', the `match.taken_vip_seats` list is updated and `client.total_tickets_vip` is incremented. Otherwise, the 
        `match.taken_general_seats` list is updated and `client.total_tickets_general` is incremented.

        Parameters:
            self (App): The App instance.

        Returns:
            None
        """
        for ticket in loaded_data.tickets:
            client = next((client for client in self.clients if client.id == ticket['client_id']), None)
    
            match = next((match for match in self.matches if match.id == ticket['match_id']), None)
            ticket_type = ticket['ticket_type']
            seat = ticket['seat']
            code = ticket['code']
            used = ticket['used']
            
            if client and match:
                ticket_object = Ticket(client, match, ticket_type, seat, code, used)
        
                # Append the ticket object correctly
                if ticket_type == 'VIP':
                    match.taken_vip_seats.append(ticket_object.seat)
                    client.total_tickets_vip += 1
                else:
                    match.taken_general_seats.append(ticket_object.seat)
                    client.total_tickets_general += 1
                
                # Update client's ticket list
                client.total_tickets += 1
                match.tickets.append(ticket_object)
                client.match_tickets.append(ticket_object)

                if ticket_object.used:
                    match.used_tickets.append(ticket_object)

    def update_products(self):
        """
        Updates the products in the App instance by iterating through the loaded product data.
        For each loaded product, it searches for a matching product in the App instance's products list.
        If a matching product is found, it updates its stock and quantity with the values from the loaded product.
        The updated product is then appended to the products_for_storing list.

        Parameters:
            self (App): The App instance.

        Returns:
            None
        """
        product_stored_data = loaded_data.products

        for loaded_product in product_stored_data:
            for stadium in self.stadiums:
                for restaurant in stadium.restaurants:
                    for product in restaurant.products:
                        self.products.append(product)
                        if product.name == loaded_product['name'] and product.adicional == loaded_product['adicional'] and product.price == loaded_product['price']:
                            product.stock = loaded_product['stock']
                            product.quantity = loaded_product['quantity']
                            self.products_for_storing.append(product)
        
                  
        
    def store_data(self):
        """
        Stores clients, tickets, and products data to JSON files after processing and updating the data accordingly.
        """
        
        # store clients data 
        clients_path = loaded_data.get_routes('clients.json')
        clients_data = [{'name': client.name, 'id': client.id, 'age': client.age, 'spent': round(client.spent, 2)} for client in self.clients]
        with open(clients_path, 'w') as f:
            json.dump(clients_data, f, indent=4)

        # store tickets data
        tickets_path = loaded_data.get_routes('tickets.json')
        tickets_data = [{'client_id': ticket.client.id, 'match_id': ticket.match.id, 'ticket_type': ticket.ticket_type, 'seat': ticket.seat, 'code': ticket.code, 'used': ticket.used} for match in self.matches for ticket in match.tickets]
        with open(tickets_path, 'w') as f:
            json.dump(tickets_data, f, indent=4)

        # store products data

        products_path = loaded_data.get_routes('products.json')

        with open(products_path, 'r') as f:
            products_data = json.load(f)
        
        # Iterate over the new products to update or append
        for bought_product in self.products_for_storing:
            new_product = {
                'name': bought_product.name,
                'quantity': bought_product.quantity,
                'stock': bought_product.stock,
                'adicional': bought_product.adicional,
                'price': bought_product.price
            }
        
            # Check if the product exists and update if found
            product_found = False
            for product in products_data:
                if product['name'] == new_product['name']:
                    product.update(new_product)
                    product_found = True
                    break
        
            # If the product does not exist, append it as a new product
            if not product_found:
                products_data.append(new_product)
        
        # Save the updated products data back to JSON file
        with open(products_path, 'w') as f:
            json.dump(products_data, f, indent=4)

    def search_team_name_matches(self, name):
        """
        Searches for matches in the matches list that match the provided name.

        Args:
            name (str): The name of the name to search for.

        Returns:
            list: A list of MatchInfo objects that match the name.
        """

        matches = [match for match in self.matches if match.local_team.name.lower() == name.lower() or match.visitor_team.name.lower() == name.lower()]
        if not matches:
            print(f"No se han encontrado partidos para el equipo de {name.lower()}")
        return matches
    
    def search_stadium_matches(self, stadium):
        """
        Searches for matches in the matches list that match the provided stadium.

        Args:
            stadium (str): The name of the stadium to search for.

        Returns:
            list: A list of MatchInfo objects that match the stadium.
        """
        matches = [match for match in self.matches if match.stadium.name.lower() == stadium.lower()]
        if not matches:
            print(f"No se han encontrado partidos en el estadio {stadium}")
        return matches
    
    def search_date_matches(self, date):
        """
        Searches for matches in the matches list that match the provided date.

        Args:
            date (str): The date to search for.

        Returns:
            list: A list of MatchInfo objects that match the date.
        """
        matches = [match for match in self.matches if match.date == date]
        if not matches:
            print(f"No se han encontrado partidos para la fecha {date}")
        return matches


    def list_all_matches(self):
        """
        Prints all the matches in the matches list.

        This method takes no parameters.

        Returns:
            None
        """
        for  i, match in enumerate(self.matches, 1):
            print(f"[{i}] {match}\n")


    # Print the map
    def create_map(self, match_id, ticket_type):
        """
        Create a map for a specific match and ticket type.

        Args:
            self: The object instance
            match_id: The ID of the match to create a map for
            ticket_type: The type of ticket to determine the capacity and taken seats

        Returns:
            None
        """
        match = next((match for match in self.matches if match.id == match_id), None)

        stadium = match.stadium
    
        if ticket_type == "VIP":
            capacity = stadium.capacity_vip
            taken_seats = match.taken_vip_seats
        else:
            capacity = stadium.capacity_general
            taken_seats = match.taken_general_seats
    
        # Define the width of each seat number for consistent formatting
        seat_width = len(str(capacity))
    
        for i in range(1, capacity + 1):
            seat_str = str(i).zfill(seat_width)
            seat_display = f"\033[31m| {seat_str} |\033[0m" if i in taken_seats else f"| {seat_str} |"
    
            # Print the seat number
            print(seat_display, end=" ") 
            # End is used to prevent the cursor from moving to the next line, it was taken from the official Python documentation
    
            # Check if we need to move to the next line
            if i % 10 == 0:
                print(f"Fila {i // 10}")
    
        # Ensure the final row label prints correctly if the last row doesn't end on a multiple of 10
        if capacity % 10 != 0:
            remaining_seats = capacity % 10
            for i in range(10 - remaining_seats):
                print(" " * (seat_width + 4), end=" ")
            print(f"Fila {(capacity // 10) + 1}")
    
    
        print()

    # Handles the purchase of a ticket for a specific match
    def create_ticket(self):
        """
        Creates a ticket for a match based on user input. The function prompts the user to enter the ID of the match they want to buy a ticket for. If the match is not found, the function prints "Partido no encontrado" and returns. The function then asks the user if they are already registered. If the user is already registered, they are prompted to enter their ID to validate their registration. If the ID is not found, the function prints "Cliente no encontrado" and returns. If the user is not registered, they are prompted to create a new client. The function checks if a client with the same ID already exists and if so, prompts the user to enter a different ID. The function then prints the client information and prompts the user to choose a ticket type and price. If the client's ID is a vampire number, the price is discounted by 50%. The function then calculates the final price including tax and prints it. The user is then prompted to confirm their purchase. If the user confirms, the function creates a map of the match and prompts the user to choose a seat. The function checks if the seat is available and if not, prompts the user to choose a different seat. Once a seat is chosen, the function creates a ticket object and updates the match and client information. The ticket is added to the list of tickets for the match and the client is added to the list of clients if they are not already in it. Finally, the function prints the ticket information and returns.
        
        Parameters:
            self (App): An instance of the App class.
        
        Returns:
            None
        """
        id = get_user_input("Para comprar una entrada, introduce el id del partido: ")
        match = next((match for match in self.matches if match.id == id), None)
        if not match:
            print("Partido no encontrado")
            return
        already_client = get_user_input("Ya estás registrado? (s/n) ", str, lambda x: is_in_options(x, ["s", "n"]))
        if already_client == 'M':
            return 
        if already_client == 's':
            client_id = get_user_input("Introduce tu ID para validar que estas registrado: ", int)
            client = next((client for client in self.clients if client.id == client_id), None)
            if not client:
                print("Cliente no encontrado")
                return
        else:
            while True:
                client = create_client()
                if any(clients.id == client.id for clients in self.clients):
                    print("Ya existe un cliente con ese ID")
                    return

        if client == 'M':
            return 'M'
            
            # Check if any existing client has the same ID as the new client
            # The any() function returns True if any element of the iterable is true. If the iterable is empty, return False.
            # Taken from the official Python documentation
                
        

        print(client)
        ticket_type, price = type_ticket()

        
        if vampire_number(client.id) == True:
            print("Felicidades, su número de cédula es un número vampiro!, disfrute de un 50% de descuento")
            price = price / 2 
            final_price = round(price * 1.16, 2)
            print(f"El costo de su entrada es de: {price}$ más el 16% de IVA para un total de \n{(final_price)}$") 
        else:
            final_price = round(price * 1.16, 2)
            print(f"El precio de la entrada {ticket_type} es: {price}$ más el 16% de IVA para un total de \n{(final_price)}$")

        print("--------------------------------------------")
        print("Seguro que desea comprar esta entrada? (s/n)")

        answer = get_user_input("", str, lambda x: is_in_options(x, ['s', 'n']), False).lower()
        # Lambda functions are small anonymous functions defined with the lambda keyword. 
        # They can have any number of arguments, but only one expression. The expression is evaluated and returned.
        # Lambda was taken from the official Python documentation.
        if answer == 'n':
            print("Entrada no comprada")
            return

        self.create_map(id, ticket_type)
        print("Coloque el número del asiento en el que quiere la entrada, si el asiento esta rojo es que no esta disponible (la fila frontal es la 1): ")
        while True:
            seat = get_user_input("", int)
    
            if seat == "M":
                return
                
            if ticket_type == "General" and (seat > match.stadium.capacity_general or seat < 1):
                print(f"Porfavor coloque un asiento entre 1 y {match.stadium.capacity_general}")
            elif ticket_type == "VIP" and (seat > match.stadium.capacity_vip or seat < 1):
                print(f"Porfavor coloque un asiento entre 1 y {match.stadium.capacity_vip}")         
            elif ticket_type == "VIP" and seat in match.taken_vip_seats:
                print("Asiento ocupado")
            elif ticket_type == "General" and seat in match.taken_general_seats:
                print("Asiento ocupado")
            else:
                break
                            
        

        ticket = Ticket(client, match, ticket_type, seat)

        # Update the stadium's taken seats and client's total tickets
        if ticket_type == "VIP":
            match.taken_vip_seats.append(seat)
            client.total_tickets_vip += 1
        else:
            match.taken_general_seats.append(seat)
            client.total_tickets_general += 1   
        
        client.spent += round(final_price, 2) # Add the cost of the ticket to the client's total spent
        client.total_tickets += 1
        client.match_tickets.append(ticket)

        # Add the ticket to the match's list of tickets
        match.tickets.append(ticket)
        print("Entrada comprada con exito!")
        print(ticket)

        # Add the client to the list of clients if it doesn't already exist
        for already_client in self.clients:
            if client.id == already_client.id:
                break
        else:
            self.clients.append(client)

    def enter_stadium(self):
        """
        Validates a user's ticket entry into a stadium.

        This function prompts the user to enter the ticket code and seat number for their entry. It then searches for a ticket with the provided code and seat number in the list of matches. If a ticket is found and it has not been used, the function sets the ticket's 'used' attribute to True and returns the client, ticket type, and restaurants associated with the stadium. If the ticket is not found or has already been used, the function prints a message indicating that the entry could not be validated and returns None.

        Parameters:
            None

        Returns:
            - If the ticket is valid and has not been used:
                - client (Client): The client associated with the ticket.
                - ticket_type (str): The type of the ticket.
                - restaurants (list): The restaurants associated with the stadium.
            - If the ticket is not found or has already been used:
                - None
        """
        ticket_code = get_user_input("Coloca el código de la entrada: ", int)
        if ticket_code == "M":
            return
            
        ticket_seat = get_user_input("Coloca el número del asiento de la entrada: ", int)
        if ticket_seat == "M":
            return
    
        ticket = next((ticket for match in self.matches for ticket in match.tickets if ticket.code == ticket_code and ticket.seat == ticket_seat), None)
    
        if ticket:
            match = next((match for match in self.matches if match == ticket.match), None)
            if ticket not in match.used_tickets:
                print("Su entrada ha sido validada")
                ticket.used = True
                match.used_tickets.append(ticket)
                return ticket.client, ticket.ticket_type, match.stadium.restaurants
        print("No ha sido posible validar su entrada")
        return None


    def menu(self):
        """
        Displays a menu of options for the user to choose from and performs the corresponding action based on the user's selection.
        
        Returns:
            None
        
        Raises:
            None
        """
        while True:
            try:
                print("-----------------------------------------")
                print("Coloca el número de lo que quieres buscar, para devolverte al menu escribe 'menu': ")
                print("1. Buscar partidas por equipo (en ingles)")
                print("2. Buscar las partidas por estadio")
                print("3. Listar partidos por fecha")
                print("4. Listar todos los partidos")
                print("5. Comprar una entrada con la id del partido")                               
                print("6. Entrar al estadio")
                print("7. Ver tus entradas")
                print("10. Salir")
                print("-----------------------------------------")
        
                option = int(input(""))
                if option == 1:
                    name = get_user_input("Coloca el nombre del equipo: ", str, validator=is_alpha)
                    if name == "M":
                        continue
                    matches = self.search_team_name_matches(name)
                    for  i, match in enumerate(matches, 1):
                        print(f"[{i}] {match}\n")
    
                elif option == 2:
                    stadium = get_user_input("Coloca el nombre del estadio: ", str)
                    if stadium == "M":
                        continue
                    matches = self.search_stadium_matches(stadium)
                    for  i, match in enumerate(matches, 1):
                        print(f"[{i}] {match}\n")
    
                elif option == 3:
                    date = get_user_input("Coloca la fecha del partido (yyyy-mm-dd): ")
                    if date == "M":
                        continue
                    matches = self.search_date_matches(date)
                    for  i, match in enumerate(matches, 1):
                        print(f"[{i}] {match}\n")
    
                elif option == 4:
                    self.list_all_matches()
    
                elif option == 5:

                    self.create_ticket()

                elif option == 6:
                    data_to_enter = self.enter_stadium()

                    if data_to_enter is not None:
                        client, ticket_type, restaurants = data_to_enter

                        if client is not None:
                            print(client)

                        if ticket_type == "VIP":
                            print("Bienvenido, su entrada es VIP, lo que significa que tiene acceso a los restaurantes!!!")
                            changed_products = restaurant_menu(client, restaurants)
                            if changed_products:
                                self.products_for_storing.extend(changed_products)
                                # The extend() method adds all elements of the iterable (in this case, changed_products) 
                                # to the end of the list (self.products_for_storing). 
                                # https://docs.python.org/3/tutorial/datastructures.html#more-on-lists

                        else:
                            print("Bienvenido, su entrada es general, no tiene acceso a los restaurantes")
                elif option == 7:
                    id = get_user_input("Coloca tu ID: ", int)
                    if id == "M":
                        continue
                    client = next((client for client in self.clients if client.id == id), None)
                    print(client)
                elif option == 10:
                    self.store_data()
                    write_statistics_to_file(self.clients, self.matches, self.products)
                    print("Hasta pronto!")
                    break
                else:
                    print("Por favor selecciona una opción válida")
            except ValueError:
                print("Porfavor introduce un valor válido")
        
