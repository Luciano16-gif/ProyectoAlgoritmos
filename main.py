# main.py
#import sys
#import os

#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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