# buyProduct.py

from funcionalidad.getUserInput import get_user_input, is_in_options
from funcionalidad.specialNumbers import is_perfect_number

def another_one():
    return get_user_input("¿Deseas otro producto? (s/n): ", str, lambda x: is_in_options(x, ["s", "n"]), False).lower()
    # Lambda functions are small anonymous functions defined with the lambda keyword. 
    # They can have any number of arguments, but only one expression. The expression is evaluated and returned.
    # Lambda was taken from the official Python documentation.

def are_you_sure():
    return get_user_input("¿Estas seguro? (s/n): ", str, lambda x: is_in_options(x, ["s", "n"]), False).lower()
    # Lambda functions are small anonymous functions defined with the lambda keyword. 
    # They can have any number of arguments, but only one expression. The expression is evaluated and returned.
    # Lambda was taken from the official Python documentation.

def validate_product(temp_products, client):
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

def show_cart(client):
    total = 0

    # Check if the cart is empty
    if len(client.cart) == 0:
        print("No hay productos en el carrito")
        return
    
    # Print the products in the cart
    for product in client.cart:
        total += product.price
        print(f"{product}")

    # Check if the client's id is a perfect number
    if is_perfect_number(client.id):
            total -= round(total * 0.15, 2)
            print("Felicidades, tu cedula es un número perfecto!!!, disfruta de un 15% de descuento")
    final_total = round(total, 2)

    print(f"Costo: {total}$ mas IVA para un total de {(final_total)}$") # print the total with IVA

    while True:
        print("-----------------------------------------")
        print("1. Borrar un producto del carrito")
        print("2. Borrar todo el carrito")
        print("3. Completar la compra")
        print("4. Salir del carrito")
        print("-----------------------------------------")

        option = get_user_input("¿Qué deseas hacer?: ", int, lambda x: is_in_options(x, [1, 2, 3]))
        if option == "M":
            return 

        if option == 1:
            delete_from_cart(client)

        if option == 2:
            if are_you_sure() == "n":
                continue 
            client.cart.clear()

        if option == 3:
            if are_you_sure() == "n":
                continue

            print("Completando la compra...")
            print("Gracias por tu compra")
            client.spent += total * 1.16 # add the total with IVA to the client's spent amount
            client.cart.clear()
            return

        if option == 4:
            return

# Delete a product from the cart
def delete_from_cart(client):
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
            
