# getuserinput.py

def get_user_input(prompt, input_type=str, validator=None, go_to_menu=True):
    """
    A function that gets user input based on the specified prompt, input type, and validator.

    Parameters:
        prompt (str): The message to display to the user.
        input_type (type, optional): The type to which the user input should be converted. Defaults to str.
        validator (function, optional): A function to validate the user input. Defaults to None.
        go_to_menu (bool, optional): A flag to allow the user to go back to the main menu. Defaults to True.

    Returns:
        The user input based on the specified input type after validation.
        'M' if the user chooses to go back to the menu.

    Raises:
        ValueError: If the user input is not valid based on the validator function.
    """
    while True:
        user_input = input(prompt)
        if go_to_menu and user_input.lower() == 'menu':
            return 'M'
        try:
            user_input = input_type(user_input)
            if validator and not validator(user_input):
                raise ValueError
            return user_input
        except ValueError:
            print("Por favor, introduce un valor válido.")

def is_alpha(string):
    """
    Check if a given string consists only of alphabetic characters.

    Args:
        string (str): The string to be checked.

    Returns:
        bool: True if the string consists only of alphabetic characters, False otherwise.
    """

    return all(char.isalpha() or char.isspace() for char in string)

def age_limit(age):
    """
    Check if the given age is within the valid range of 0 to 130.

    Args:
        age (int): The age to be checked.

    Returns:
        bool: True if the age is within the valid range, False otherwise.
    """
    if age < 0 or age > 130:
        print("Porfavor introduce una edad entre 0 y 130")
        return False
    return True

def id_check(id):
    """
    Check if the given ID is within the valid range of 1 to 2000000000.

    Args:
        id (int): The ID to be checked.

    Returns:
        bool: True if the ID is within the valid range, False otherwise.
    """
    if id < 1 or id > 2000000000:
        print("Porfavor introduce un ID entre 1 y 2000000000")
        return False
    return True

def name_model(name):
    """
    Converts a given name to a standardized format by converting all letters to lowercase
    and capitalizing the first letter.

    Args:
        name (str): The name to be standardized.

    Returns:
        str: The standardized name.
    """
    name = name.lower()
    name = name[0].upper() + name[1:]
    return name

def is_in_options(option, options):
    """
    Check if the given option is present in the options list.

    Args:
        option (str or any): The option to be checked.
        options (list): The list of options.

    Returns:
        bool: True if the option is present in the options list, False otherwise.
    """

    if isinstance(option, str):
        option = option.lower()

    if option not in options:
        return False
    return True