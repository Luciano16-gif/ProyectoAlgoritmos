# stadium.py

class Product:
    def __init__(self, name, quantity, price, stock, adicional):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.stock = stock
        self.adicional = adicional

    def __str__(self):
        if self.stock > 0:
            return f"{self.name} - {self.price}$ ({self.stock} en stock)"
        else:
            return f"{self.name} - {self.price}$ (No hay stock)"


class Restaurant:
    def __init__(self, name, products):
        self.name = name
        self.products = [Product(**product) for product in products]

    def __str__(self):
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