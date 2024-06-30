# main.py

from funcionalidad.App import App
import requests

data = {
    "teams": [],
    "stadiums": [],
    "matches": []
}

def fetch_data(url, key):
    """
    Fetches data from the specified URL and stores it in the global data dictionary under the given key.
    
    Parameters:
        url (str): The URL from which to fetch the data.
        key (str): The key under which to store the fetched data in the global data dictionary.
    
    Returns:
        None
    
    Raises:
        requests.RequestException: If there is an error while fetching the data.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        data[key] = response.json()
    except requests.RequestException as e:
        print(f"Error al obtener los datos de {key}: {e}")

def main():
    """
    Fetches data from the specified URLs and initializes an App instance with the fetched data.
    
    This function defines a dictionary of URLs for different data types, such as teams, stadiums, and matches.
    It then iterates over the dictionary, calling the fetch_data function for each URL to fetch the data.
    After fetching all the data, it initializes an App instance with the fetched data and prints "Funcionando".
    Finally, it calls the menu method of the App instance.
    """
    urls = {
        "teams": "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/teams.json",
        "stadiums": "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/stadiums.json",
        "matches": "https://raw.githubusercontent.com/Algoritmos-y-Programacion/api-proyecto/main/matches.json"
    }

    for key, url in urls.items():
        fetch_data(url, key)

    app = App(data)
    print("Funcionando")

    app.menu()

if __name__ == "__main__":
    main()