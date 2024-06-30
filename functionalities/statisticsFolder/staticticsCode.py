import os
import matplotlib.pyplot as plt

def calculate_vip_spending_average(clients):
    """
    Calculates the average spending of VIP clients based on their total spending.
    
    Parameters:
    clients (list): A list of client objects.
    
    Returns:
    float: The average spending of VIP clients rounded to 2 decimal places. Returns 0 if there are no VIP clients.
    """
    total_spent = 0
    total_vip_clients = 0
    
    for client in clients:
        if client.total_tickets_vip > 0:
            total_spent += client.spent
            total_vip_clients += 1
            
    return round(total_spent / total_vip_clients, 2) if total_vip_clients > 0 else 0

def generate_match_attendance_table(matches):
    """
    Generates a table of match attendance data for a list of matches.
    
    Args:
    matches (list): A list of match objects.
    
    Returns:
    list: A list of dictionaries containing information about each match, including the match name, stadium name,
    number of tickets sold, number of people who attended the match, and the attendance ratio. The list is sorted
    in descending order based on the attendance ratio.
    """
    attendance_data = []
    for match in matches:
        total_tickets_sold = len(match.tickets)
        total_attendance = len(match.used_tickets)
        attendance_ratio = total_attendance / total_tickets_sold if total_tickets_sold > 0 else 0
        attendance_data.append({
            "match_name": f"{match.local_team.name} vs {match.visitor_team.name}",
            "stadium": match.stadium.name,
            "tickets_sold": total_tickets_sold,
            "attendance": total_attendance,
            "attendance_ratio": attendance_ratio
        })
    
    attendance_data.sort(key=lambda x: x["attendance_ratio"], reverse=True)
    return attendance_data

def find_highest_attendance_match(matches):
    """
    Find the match with the highest attendance in a list of matches.

    Parameters:
        matches (list): A list of match objects.

    Returns:
        match: The match object with the highest attendance. If the list is empty, None is returned.
    """
    return max(matches, key=lambda match: len(match.used_tickets), default=None)
    # The max function returns the match with the highest number of used tickets (attendance).
    # If the matches list is empty, it returns None as specified by the default parameter.
    # https://docs.python.org/3/library/functions.html#max

def find_highest_tickets_sold_match(matches):
    """
    Find the match with the highest number of tickets sold in a list of matches.

    Parameters:
        matches (list): A list of match objects.

    Returns:
        match: The match object with the highest number of tickets sold. If the list is empty, None is returned.
    """
    return max(matches, key=lambda match: len(match.tickets), default=None)

def find_top_selling_products(products):
    top_sellin = []
    """
    Sorts the list of products in descending order based on the quantity sold.
    Returns the top 3 selling products.

    Parameters:
        products (list): A list of product objects.

    Returns:
        list: A list of the top 3 selling products.
    """
    products.sort(key=lambda product: product.quantity, reverse=True)
    for i in range(len(products)):
        if products[i] not in top_sellin:
            top_sellin.append(products[i])
            print(products[i])
            if len(top_sellin) == 3:
                break
    return top_sellin
   

def find_top_clients(clients):
    """
    Sorts the list of clients in descending order based on the total number of tickets they have.
    Returns the top 3 clients with the highest total number of tickets.

    Parameters:
        clients (list): A list of client objects.

    Returns:
        list: A list of the top 3 clients with the highest total number of tickets.
    """
    clients.sort(key=lambda client: client.total_tickets, reverse=True)
    return clients[:3]

script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, "statistics.txt")
graphs_dir = os.path.join(script_dir, "graphs")
os.makedirs(graphs_dir, exist_ok=True)

def create_and_save_graphs(clients, matches, products):
    """
    Generates and saves three graphs:
    - Graph for match attendance: Shows the attendance ratio for each match.
    - Graph for top 3 selling products: Shows the quantity sold for the top 3 selling products.
    - Graph for top 3 clients: Shows the number of tickets bought by the top 3 clients.
    
    Parameters:
    - clients (list): A list of client objects.
    - matches (list): A list of match objects.
    - products (list): A list of product objects.
    
    Returns:
    - None
    """

    # Matplotlib is a plotting library for Python and its numerical mathematics extension NumPy.
    # Official Matplotlib documentation: https://matplotlib.org/stable/users/index.html
    
    # 1. Graph for match attendance
    attendance_table = generate_match_attendance_table(matches)
    match_names = [entry["match_name"] for entry in attendance_table]
    attendance_ratios = [entry["attendance_ratio"] * 100 for entry in attendance_table]
    fig, ax = plt.subplots()
    ax.barh(match_names, attendance_ratios)
    ax.set_xlabel('Relación asistencia/venta (%)')
    ax.set_title('Tabla de asistencia porcentual a los partidos')
    plt.savefig(os.path.join(graphs_dir, "match_attendance.png"))
    plt.close(fig)
    
    # 2. Graph for top 3 selling products
    top_products = find_top_selling_products(products)
    product_names = [product.name for product in top_products]
    product_quantities = [product.quantity for product in top_products]
    fig, ax = plt.subplots()
    ax.bar(product_names, product_quantities)
    ax.set_ylabel('Cantidad vendida')
    ax.set_title('Top 3 productos más vendidos en el restaurante')
    plt.savefig(os.path.join(graphs_dir, "top_selling_products.png"))
    plt.close(fig)
    
    # 3. Graph for top 3 clients
    top_clients = find_top_clients(clients)
    client_names = [client.name for client in top_clients]
    tickets_bought = [client.total_tickets for client in top_clients]
    fig, ax = plt.subplots()
    ax.bar(client_names, tickets_bought)
    ax.set_ylabel('Boletos comprados')
    ax.set_title('Top 3 clientes (que más compraron boletos)')
    plt.savefig(os.path.join(graphs_dir, "top_clients.png"))
    plt.close(fig)

def write_statistics_to_file(clients, matches, products):
    """
    Writes statistics to a file.

    Args:
        clients (list): A list of client objects.
        matches (list): A list of match objects.
        products (list): A list of product objects.

    Returns:
        None

    This function writes statistics to a file in the following format:

    1. Average VIP spending: The average spending of VIP clients in a match.

    2. Match attendance table: A table showing the attendance percentage of each match, sorted from best to worst.

    3. Match with highest attendance: The match with the highest attendance, along with the number of tickets sold.

    4. Match with highest tickets sold: The match with the highest number of tickets sold, along with the number of tickets sold.

    5. Top 3 selling products: The top 3 products sold in the restaurant, along with the quantity sold.

    6. Top 3 clients: The top 3 clients who bought the most tickets, along with the number of tickets bought.

    The statistics are written to a file specified by the `file_path` variable. The file is opened in write mode with UTF-8 encoding.

    After writing the statistics to the file, the function calls `create_and_save_graphs` to create and save graphs for the top 3 selling products and top 3 clients.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        # 1. Average VIP spending
        vip_spending_avg = calculate_vip_spending_average(clients)
        file.write(f"Promedio de gasto de un cliente VIP en un partido: {vip_spending_avg}$\n\n")
        
        # 2. Match attendance table
        file.write("Tabla de asistencia porcentual a los partidos (mejor a peor):\n")
        attendance_table = generate_match_attendance_table(matches)
        for i, entry in enumerate(attendance_table, 1):
            file.write(f"[{i}] {entry['match_name']} en {entry['stadium']}: "
                       f"Boletos vendidos: {entry['tickets_sold']}, "
                       f"Personas que asistieron: {entry['attendance']}, "
                       f"Relación asistencia/venta: {entry['attendance_ratio'] * 100:.2f}%\n")
        file.write("\n")
        
        # 3. Match with highest attendance
        highest_attendance_match = find_highest_attendance_match(matches)
        if highest_attendance_match:
            file.write(f"Partido con mayor asistencia: {highest_attendance_match.local_team.name} vs "
                       f"{highest_attendance_match.visitor_team.name} con {len(highest_attendance_match.used_tickets)}\n\n")
        
        # 4. Match with highest tickets sold
        highest_tickets_sold_match = find_highest_tickets_sold_match(matches)
        if highest_tickets_sold_match:
            file.write(f"Partido con mayor boletos vendidos: {highest_tickets_sold_match.local_team.name} vs "
                       f"{highest_tickets_sold_match.visitor_team.name} con {len(highest_tickets_sold_match.tickets)}\n\n")
        
        # 5. Top 3 selling products
        top_products = find_top_selling_products(products)
        file.write("Top 3 productos más vendidos en el restaurante:\n")
        for product in top_products:
            file.write(f"{product.name} - Cantidad vendida: {product.quantity}\n")
        file.write("\n")
        
        # 6. Top 3 clients
        top_clients = find_top_clients(clients)
        file.write("Top 3 clientes (que más compraron boletos):\n")
        for client in top_clients:
            file.write(f"{client.name} - Boletos comprados: {client.total_tickets}\n")
        file.write("\n")

    # Create and save graphs
    create_and_save_graphs(clients, matches, products)
