from gestionDePartidosyEstadios.MatchInfo import MatchInfo
from gestionDePartidosyEstadios.stadium import Stadium
from gestionDePartidosyEstadios.teams import Teams
from gestionDeClientes.client import Client
from gestionDeClientes.ticket import Ticket
from funcionalidad.buyTicket import create_client, type_ticket, vampire_number, is_alpha, get_user_input, name_model


class App:
    def __init__(self, data) -> None:
        """
        Initializes a new instance of the App class.

        Args:
            data (dict): La data que contiene el JSON.

        Returns:
            None
        """
        self.data = data
        self.teams = []
        self.stadiums = []
        self.matches = []
        self.clients = []
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
    def create_ticket(self, id):
        match = next((match for match in self.matches if match.id == id), None)
        if not match:
            print("Partido no encontrado")
            return
        while True:
            client = create_client()

            if client == 'M':
                return 'M'
            
            # Check if any existing client has the same ID as the new client
            # The any() function returns True if any element of the iterable is true. If the iterable is empty, return False.
            # Taken from the official Python documentation
            if any(existing_client.id == client.id for existing_client in self.clients):
                print("Ya existe un cliente con ese ID. Por favor, intente con otro ID.")
            else:
                break
                
        

        print(client)
        ticket_type, price = type_ticket()

        
        if vampire_number(client.id) == True:
            print("Felicidades, su número de cédula es un número vampiro!, disfrute de un 50% de descuento")
            discounted_price = price / 2 
            print(f"El costo de su entrada es de: {discounted_price:.2f}$ más el 16% de IVA para un total de \n{(discounted_price * 1.16):.2f}$") 
            # the ":.2f" part is to round the number to 2 decimal places
        else:
            print(f"El precio de la entrada {ticket_type} es: {price}$ más el 16% de IVA para un total de \n{(price * 1.16):.2f}$")

        print("--------------------------------------------")
        print("Seguro que desea comprar esta entrada? (s/n)")
        while True:
            try:
                answer = str(input())
                if answer.lower() not in ['s', 'n']:
                    print("Porfavor introduce s o n")
                else:
                    if answer.lower() == 's':
                        break
                    else:
                        print("Entrada no comprada")
                        return
            except ValueError:
                print("Porfavor introduce un valor válido")

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
        match_id = get_user_input("Coloca el ID del partido: ")
        if match_id == "M":
            return
        match = next((match for match in self.matches if match.id == match_id), None)
        if not match:
            print("Partido no encontrado")
            return
            
        ticket_code = get_user_input("Coloca el código de la entrada: ", int)
        if ticket_code == "M":
            return
            
        ticket_seat = get_user_input("Coloca el número del asiento de la entrada: ", int)
        if ticket_seat == "M":
            return

        ticket = next((ticket for ticket in match.tickets if ticket.code == ticket_code and ticket.seat == ticket_seat), None)

        if ticket is not None and ticket not in match.used_tickets:
            print("Su entrada ha sido validada")
            print(ticket)
            match.used_tickets.append(ticket)
            return ticket.client
        else:
            print("No ha sido posible validar su entrada")

            
                
                

    def menu(self):
        while True:
            try:
                print("-----------------------------------------")
                print("Coloca el número de lo que quieres buscar, para devolverte al menu escribe 'menu': ")
                print("1. Buscar partidas por equipo")
                print("2. Buscar las partidas por estadio")
                print("3. Listar partidos por fecha")
                print("4. Listar todos los partidos")
                print("5. Comprar una entrada")
                print("6. Entrar al estadio")
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
                    id = get_user_input("Para comprar una entrada, introduce el id del partido: ")
                    if id == "M":
                        continue
                    self.create_ticket(id)

                elif option == 6:
                    client = self.enter_stadium()
                    if client is not None:
                        print(client)
    
                elif option == 10:
                    print("Hasta pronto!")
                    break
                else:
                    print("Por favor selecciona una opción válida")
            except ValueError:
                print("Porfavor introduce un valor válido")
        
