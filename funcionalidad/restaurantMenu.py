#restaurantMenu.py

from funcionalidad.getUserInput import get_user_input, is_in_options, is_alpha
from funcionalidad.buyProduct import validate_product, show_cart


def restaurant_menu(client, restaurants):
    """
    Runs the restaurant menu for a given client and list of restaurants.

    Args:
        client (Client): The client object.
        restaurants (List[Restaurant]): The list of restaurant objects.

    Returns:
        List[Product]: The list of changed products.

    Description:
        This function displays the restaurant menu options to the user and allows them to search for products by name, type, price range, or list all products. 
        It also provides options to view all available restaurants and their products, view the shopping cart, complete the purchase, and delete products from 
        the shopping cart. The function returns a list of changed products.
    """
    changed_products = []
    temp_products = []
    while True:
        print("-----------------------------------------")
        print("Coloca el número de lo que quieres buscar, para devolverte a este menu escribe 'menu': ")
        print("Recomendación: Primero selecciona 5 para ver todos los productos")
        print("1. Buscar por nombre para comprar")
        print("2. Buscar por tipo para comprar")
        print("3. Buscar por rango de precio para comprar")
        print("4. Listar todos los productos para comprar")
        print("5. Ver todos los restaurantes disponibles y sus productos")
        print("6. Ver carrito, completar compra, borrar productos del carrito")
        print("7. Salir")
        print("-----------------------------------------")

        option = get_user_input("", int, False)
        if option == 1:
            name = get_user_input("Coloca el nombre de lo que desee comprar: ", str, validator=is_alpha)

            if name == "M":
                continue

            for restaurant in restaurants:
                for product in restaurant.products:
                    if name.lower() in product.name.lower():
                        temp_products.append(product)

            if not temp_products:
                print("No se han encontrado resultados")
                continue
            else:
                for i, product in enumerate(temp_products, 1):
                    print(f"[{i}] {product}")
            
            validate_product(temp_products, client)

        elif option == 2:
            # Search by type
            
            adicional_values = ["plate", "package", "alcoholic", "non-alcoholic"] # list of the true values of adicional
            additional_names = ["Plato", "Paquete", "Bebida alcoholica", "Bebida no alcoholica"] # list of the names that will be shown

            for i, adittional in enumerate(additional_names, 1):
                print(f"[{i}] {adittional}")

            print("Ponga el número del tipo de producto que desea comprar")

            option = get_user_input("", int, lambda x: is_in_options(x, [1, 2, 3, 4]))
            if option == "M":
                continue
            product_type = adicional_values[option - 1] # get the true value of adicional


            for restaurant in restaurants:
                for product in restaurant.products:
                    if product_type in product.adicional:
                        temp_products.append(product)

            if not temp_products:
                print("No se han encontrado resultados")
                continue
            else:
                for i, product in enumerate(temp_products, 1):
                    print(f"[{i}] {product}")

            validate_product(temp_products, client)

        elif option == 3:
            # Search by price range
            print("Ponga el rango de precio que desea comprar")
            min_price = get_user_input("Precio mínimo: ", int, lambda x: x >= 0)
            if min_price == "M":
                continue
            max_price = get_user_input("Precio máximo: ", int, lambda x: x >= min_price)
            if max_price == "M":
                continue
            

            for restaurant in restaurants:
                for product in restaurant.products:
                    if min_price <= product.price <= max_price:
                        temp_products.append(product)

            if not temp_products:
                print("No se han encontrado resultados")
                continue
            else:
                for i, product in enumerate(temp_products, 1):
                    print(f"[{i}] {product}")
            
            validate_product(temp_products, client)
        elif option == 4:
            # List all products
            for restaurant in restaurants:
                for i, product in enumerate(restaurant.products, 1):
                    temp_products.append(product)

            if not temp_products:
                print("No se han encontrado resultados")
                continue
            else:
                for i, product in enumerate(temp_products, 1):
                    print(f"[{i}] {product}")

            validate_product(temp_products, client)
        elif option == 5:
            for restaurant in restaurants:
                print(restaurant)
        elif option == 6:
            bought_products = show_cart(client)
            if bought_products:
                changed_products.extend(bought_products)
            
        elif option == 7:
            print("Hasta pronto!!!")
            return changed_products
        else:
            print("Porfavor coloque una opcion válida") 