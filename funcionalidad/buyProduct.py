# buyProduct.py

from funcionalidad.getUserInput import get_user_input, is_in_options

def another_one():
    return get_user_input("¿Deseas otro producto? (s/n): ", str, lambda x: is_in_options(x, ["s", "n"])).lower()

def validate_product(temp_products, client):
    while True:
        product = get_user_input("", int)
        if product == "M":
            return 'M'
        
        if product > len(temp_products) or product < 1:
            print("Porfavor coloque un plato valido")
        else:
            product = temp_products[product - 1]
            if product.stock == 0:
                print(f"El producto {product.name} no tiene stock")
            if product.adicional == "alcoholic" and client.age < 18:
                print(f"El plato {product.name} no es apto para menores de 18")
            else:
                client.cart.append(product)
                print(f"Plato {product.name} añadido al carrito")
                
                if another_one().lower() == "n":
                    break

