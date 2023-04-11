import requests

base_url = "http://localhost:5000"

# Test de l'API airport_list
response = requests.get(f"{base_url}/api/airport_list")
if response.status_code == 200:
    print("API airport_list:")
    print(response.json())
else:
    print(f"Erreur lors de l'appel de l'API airport_list: {response.status_code}")

# Test de l'API year_list avec un code d'aéroport
airport_code = "JFK"  # Remplacez par un code d'aéroport valide dans votre dataset
response = requests.get(f"{base_url}/api/year_list", params={"airport_code": airport_code})
if response.status_code == 200:
    print(f"\nAPI year_list pour l'aéroport {airport_code}:")
    print(response.json())
else:
    print(f"Erreur lors de l'appel de l'API year_list: {response.status_code}")

# Test de l'API airport_delay_trend avec un code d'aéroport et une année
year = 2019  # Remplacez par une année valide dans votre dataset
response = requests.get(f"{base_url}/api/airport_delay_trend", params={"airport_code": airport_code, "year": year})
if response.status_code == 200:
    print(f"\nAPI airport_delay_trend pour l'aéroport {airport_code} en {year}:")
    print(response.json())
else:
    print(f"Erreur lors de l'appel de l'API airport_delay_trend: {response.status_code}")
