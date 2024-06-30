import os
import json
from clientManagement.client import Client

class Stored_Data():
    def __init__(self):
        """
        Initializes a new instance of the class.

        This method initializes the `clients`, `tickets`, and `products` attributes to empty lists. It then calls the `load_data` method to load data from JSON files into these attributes.

        Parameters:
            None

        Returns:
            None
        """
        self.clients = []
        self.tickets = []
        self.products = []
        self.load_data()


    def get_routes(self, json_file):
        """
        Returns the absolute path to a JSON file stored in the 'saved_data' directory of the project root.

        :param json_file: The name of the JSON file to retrieve.
        :type json_file: str
        :return: The absolute path to the JSON file.
        :rtype: str
        """
        # Get the directory of the current script
        script_dir = os.path.dirname(__file__)
        
        # Move up one directory level to get the project root directory
        project_root = os.path.abspath(os.path.join(script_dir, os.pardir))

        new_path = os.path.join(project_root, 'saved_data', json_file)

        return new_path

    def load_data(self):
        """
        Loads data from JSON files into the `clients`, `tickets`, and `products` attributes.
        """
        
        # Construct the path to the clients.json file relative to the project root
        clients_path = self.get_routes('clients.json')
        with open(clients_path) as f:
            clients_data = json.load(f)
            self.clients = [Client(**client) for client in clients_data]
        
        # Construct the path to the tickets.json file relative to the project root
        tickets_path = self.get_routes('tickets.json')
        with open(tickets_path) as f:
            tickets_data = json.load(f)
            self.tickets = tickets_data

        product_path = self.get_routes('products.json')
        with open(product_path) as f:
            products_data = json.load(f)
            self.products = products_data

        