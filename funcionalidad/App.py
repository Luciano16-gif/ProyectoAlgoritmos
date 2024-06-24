from gestionDePartidosyEstadios.MatchInfo import MatchInfo
from gestionDePartidosyEstadios.stadium import Stadium
from gestionDePartidosyEstadios.teams import Teams
from gestionDeClientes.client import Client
from gestionDeClientes.ticket import Ticket
from funcionalidad.buyTicket import create_client, type_ticket, vampire_number


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
            self.stadiums.append(Stadium(stadium['id'],stadium['name'], stadium['city'], stadium['capacity'][0], stadium['capacity'][1]))

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

    def get_user_input(self, prompt, type=str):
        while True:
            try:
                return type(input(prompt))
            except ValueError:
                print("Por favor, introduce un valor válido.")

    def search_team_name_matches(self, name):
        """
        Searches for matches in the matches list that match the provided name.

        Args:
            name (str): The name of the name to search for.

        Returns:
            list: A list of MatchInfo objects that match the name.
        """

        matches = [match for match in self.matches if match.local_team.name == name or match.visitor_team.name == name]
        if not matches:
            print(f"No se han encontrado partidos para el equipo de {name}")
        return matches
    
    def search_stadium_matches(self, stadium):
        """
        Searches for matches in the matches list that match the provided stadium.

        Args:
            stadium (str): The name of the stadium to search for.

        Returns:
            list: A list of MatchInfo objects that match the stadium.
        """
        matches = [match for match in self.matches if match.stadium.name == stadium]
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
        for match in self.matches:
            print(match)


    
    def create_map(self, match_id, ticket_type):
        match = next((match for match in self.matches if match.id == match_id), None)

        stadium = match.stadium
    
        if ticket_type == "VIP":
            capacity = stadium.capacity_vip
            taken_seats = stadium.taken_vip_seats
        else:
            capacity = stadium.capacity_general
            taken_seats = stadium.taken_general_seats
    
        # Define the width of each seat number for consistent formatting
        seat_width = len(str(capacity))
    
        for i in range(1, capacity + 1):
            seat_str = str(i).zfill(seat_width)
            seat_display = f"\033[31m| {seat_str} |\033[0m" if i in taken_seats else f"| {seat_str} |"
    
            # Print the seat number
            print(seat_display, end=" ")
    
            # Check if we need to move to the next line
            if i % 10 == 0:
                print(f"Fila {i // 10}")
    
        # Ensure the final row label prints correctly if the last row doesn't end on a multiple of 10
        if capacity % 10 != 0:
            remaining_seats = capacity % 10
            for i in range(10 - remaining_seats):
                print("       ", end=" ")
            print(f"Fila {(capacity // 10) + 1}")
    
        print()

    def create_ticket(self, id):
        match = next((match for match in self.matches if match.id == id), None)
        if match is None:
            print("Partido no encontrado")
            return
        client = create_client()
        print(client)
        ticket_type, price = type_ticket()

        
        if vampire_number(client.id) == True:
            print("Felicidades, su número de cédula es un número vampiro!, disfrute de un 50% de descuento")
            discounted_price = price / 2 
            print(f"El costo de su entrada es de: {discounted_price:.2f}$ más el 16% de IVA para un total de \n{(discounted_price * 1.16):.2f}$")
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
        try:
            seat = self.get_user_input("", int)
        except ValueError:
            print("Porfavor introduce un valor numerico")
        
        if ticket_type == "VIP":
            match.stadium.taken_vip_seats.append(seat)
        else:
            match.stadium.taken_general_seats.append(seat)

        ticket = Ticket(client, match, ticket_type, seat)
        match.tickets.append(ticket)
        print("Entrada comprada con exito!")
        print(ticket)

        if client not in self.clients:
            self.clients.append(client)
        

    def menu(self):
        while True:
            print("-----------------------------------------")
            print("Coloca el número de lo que quieres buscar: ")
            print("1. Buscar partidas por equipo")
            print("2. Buscar las partidas por estadio")
            print("3. Listar partidos por fecha")
            print("4. Listar todos los partidos")
            print("5. Comprar una entrada")
            print("10. Salir")
            print("-----------------------------------------")
    
            option = self.get_user_input("", int)
            if option == 1:
                name = self.get_user_input("Coloca el nombre del equipo: ")
                matches = self.search_team_name_matches(name)
                for match in matches:
                    print(match)
            elif option == 2:
                stadium = input("Coloca el nombre del estadio: ")
                matches = self.search_stadium_matches(stadium)
                print(matches)
            elif option == 3:
                date = self.get_user_input("Coloca la fecha del partido (yyyy-mm-dd): ")
                matches = self.search_date_matches(date)
                for match in matches:
                    print(match)
            elif option == 4:
                self.list_all_matches()
            elif option == 5:
                id = self.get_user_input("Para comprar una entrada, introduce el id del partido: ")
                self.create_ticket(id)
            elif option == 10:
                break
            else:
                print("Por favor selecciona una opción válida")
    
    
