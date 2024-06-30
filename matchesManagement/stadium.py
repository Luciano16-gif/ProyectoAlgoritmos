# stadium.py

class Product:
    def __init__(self, name, quantity, price, stock, adicional):
        """
        Initializes the Product object with the given parameters.

        Parameters:
            name (str): The name of the product.
            quantity (int): The quantity of the product.
            price (float): The price of the product.
            stock (int): The stock of the product.
            adicional (str): The additional information about the product.

        Returns:
            None
        """
        self.name = name
        self.quantity = int(quantity)
        self.price = float(price)
        self.stock = int(stock)
        self.adicional = adicional

    def __str__(self):
        """
        Returns a string representation of the Product object.

        Returns:
            str: The string representation of the Product object.
                If the stock is greater than 0, it returns the name, price, stock, and adicional.
                If the stock is 0, it returns the name and price with a message indicating that there is no stock.
        """
        if self.stock > 0:
            return f"{self.name} - {self.price}$ ({self.stock} en stock), Tipo: {self.adicional}"
        else:
            return f"{self.name} - {self.price}$ (No hay stock)"


class Restaurant:
    def __init__(self, name, products):
        """
        Initializes the Restaurant object with the given parameters.

        Parameters:
            name (str): The name of the restaurant.
            products (list): A list of dictionaries representing products. Each dictionary contains information about a product.

        Returns:
            None
        """
        self.name = name
        self.products = [Product(**product) for product in products]

    def __str__(self):
        """
        Returns a string representation of the Restaurant object.

        Returns:
            str: The string representation of the Restaurant object.
                It includes the name of the restaurant and a formatted list of products.
        """
        productos_str = "\n  ".join([f"[{i}] {product}" for i, product in enumerate(self.products, 1)])
        # .join() was taken out of the official python documentation
        return f"{self.name} con productos:\n  {productos_str}"
    
    def show_name(self):
        return f"{self.name}"


class Stadium:
    def __init__(self, id, name, location, capacity_general, capacity_vip, restaurants) -> None:
        self.id = id
        self.name = name
        self.location = location
        self.capacity_general = capacity_general
        self.capacity_vip = capacity_vip
        self.restaurants = [Restaurant(**restaurant) for restaurant in restaurants]

    def __str__(self) -> str:
        restaurantes_str = "\n  ".join([str(f"{restaurant}\n") for restaurant in self.restaurants])
        return f"Estadio: {self.name}, Ubicación: {self.location}\n Restaurantes:\n  {restaurantes_str}"
    
    def show_name(self):
        return f"{self.name}"