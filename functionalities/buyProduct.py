# buyProduct.py

from functionalities.getUserInput import get_user_input, is_in_options
from functionalities.specialNumbers import is_perfect_number

def another_one():
    """
    Prompts the user to input whether they want to buy another product.

    Returns:
        str: The lowercase input from the user.
    """
    return get_user_input("¿Deseas otro producto? (s/n): ", str, lambda x: is_in_options(x, ["s", "n"]), False).lower()
    # Lambda functions are small anonymous functions defined with the lambda keyword. 
    # They can have any number of arguments, but only one expression. The expression is evaluated and returned.
    # Lambda was taken from the official Python documentation.

def are_you_sure():
    """
    Prompts the user to confirm an action.

    This function displays a message asking the user if they are sure about an action. It uses the `get_user_input` function to get the user's input as a string. The input is validated using a lambda function that checks if the input is either "s" or "n". The input is converted to lowercase before being returned.

    Returns:
        str: The lowercase input from the user.
    """
    return get_user_input("¿Estas seguro? (s/n): ", str, lambda x: is_in_options(x, ["s", "n"]), False).lower()

def validate_product(temp_products, client):
    """
    Validates a product for addition to the client's shopping cart.

    Args:
        temp_products (list): A list of temporary products.
        client (Client): The client object.

    Returns:
        None: If the user chooses to go back to the main menu.

    This function prompts the user to input the number of the product they want to add to their shopping cart. It validates the input by checking if it is 
    within the range of available products. If the product has no stock or is not suitable for the client's age, an appropriate message is displayed. If the 
    product is valid, it is added to the client's shopping cart. The user is then prompted to add another product or go back to the main menu.

    Note:
        - The function uses the `get_user_input` function to get user input.
        - The function clears the temporary products list if the user chooses not to add another product.
        - The function breaks the loop if the user chooses to go back to the main menu.
    """
    print("Ponga el número del producto que desee agregar a la compra, para devolverte a este menu escribe 'menu': ")

    while True:
        product = get_user_input("", int)
        if product == "M":
            return 
        
        if product > len(temp_products) or product < 1:
            print("Porfavor coloque un producto valido")
        else:
            product = temp_products[product - 1]
            if product.stock == 0:
                print(f"El producto {product.name} no tiene stock")
            if product.adicional == "alcoholic" and client.age < 18:
                print(f"El plato {product.name} no es apto para menores de 18")
            else:
                client.cart.append(product)
                print(f"Producto {product.name} añadido al carrito")
                
                if another_one().lower() == "n":
                    temp_products.clear()
                    break
                else:
                    print("Coloque el número del producto que desee agregar al carrito")

def show_cart(client):
    """
    A function that displays the client's shopping cart, calculates the total price with discounts, and allows various actions such as deleting products, 
    completing the purchase, or exiting the cart. It prompts the user for options to interact with the cart, such as deleting a product, clearing the cart, 
    completing the purchase, or exiting. The function checks if the cart is empty, calculates the total price with possible discounts, 
    and handles stock management for products in the cart. It returns a list of sold products after completing the purchase.

    Parameters:
        client (Client): The client object.

    Returns:
        List: A list of sold products after completing the purchase or None if the user chooses to exit.
    """
    while True:
        total = 0
    
        # Check if the cart is empty
        if len(client.cart) == 0:
            print("No hay productos en el carrito")
            return
        
        # Print the products in the cart
        for i, product in enumerate(client.cart, 1):
            total += product.price
            print(f"[{i}] {product}")
    
        # Check if the client's id is a perfect number
        print(is_perfect_number(client.id))
        if is_perfect_number(client.id):
                total -= round(total * 0.15, 2)
                print("Felicidades, tu cedula es un número perfecto!!!, disfruta de un 15% de descuento")
        final_total = round(total * 1.16, 2)
    
        print(f"Costo: {total}$ mas IVA para un total de {(final_total)}$") # print the total with IVA
    
        print("-----------------------------------------")
        print("1. Borrar un producto del carrito")
        print("2. Borrar todo el carrito")
        print("3. Completar la compra")
        print("4. Salir del carrito")
        print("-----------------------------------------")

        option = get_user_input("¿Qué deseas hacer?: ", int)
        if option == "M":
            return 

        if option == 1:
            delete_from_cart(client)

        elif option == 2:
            if are_you_sure() == "n":
                continue 
            client.cart.clear()
            return

        elif option == 3:
            if are_you_sure() == "n":
                continue

            sold_products = []
            
            for product in client.cart:
                if product.stock <= 0:
                    print(f"No hay suficiente stock de {product.name}")
                    return
                product.stock -= 1
                product.quantity += 1

            for product in client.cart:
                if client.cart.count(product) > 1:
                    client.cart.remove(product)
                
                print(product)
                sold_products.append(product)

            print("Completando la compra...")
            print("Gracias por tu compra")
            client.spent += round(final_total, 2) # add the total with IVA to the client's spent amount
            client.cart.clear()
            return sold_products

        elif option == 4:
            return
        else:
            print("Porfavor coloque una opción valida")

# Delete a product from the cart
def delete_from_cart(client):
    """
    Deletes a product from the client's shopping cart.

    Args:
        client (Client): The client object.

    Returns:
        str: 'M' if the user wants to return to the main menu.
    """
    while True:
        product = get_user_input("Coloque el número del producto que desea borrar: ", int)
        if product == "M":
            return 'M'

        if product > len(client.cart) or product < 1:
            print("Porfavor coloque un producto valido")
        elif are_you_sure() == "n":
            return
        else:
            product = client.cart[product - 1]
            client.cart.remove(product)
            print(f"Producto {product.name} eliminado del carrito")
            return
            
            
