import requests

base_url = "http://localhost:5000"

# Test de l'API airport_dep_list
response = requests.get(f"{base_url}/api/airport_dep_list")
if response.status_code == 200:
    print("API airport_dep_list:")
    print(response.json())
else:
    print(f"Erreur lors de l'appel de l'API airport_dep_list: {response.status_code}")

# Test de l'API airport_dest_list
response = requests.get(f"{base_url}/api/airport_dest_list")
if response.status_code == 200:
    print("API airport_dest_list:")
    print(response.json())
else:
    print(f"Erreur lors de l'appel de l'API airport_dest_list: {response.status_code}")

# Test de l'API airport_dep_delay_trend avec un code d'aéroport
airport_code = "JFK"  # Remplacez par un code d'aéroport valide dans votre dataset
response = requests.get(f"{base_url}/api/airport_dep_delay_trend", params={"airport_code": airport_code})
if response.status_code == 200:
    print(f"\nAPI airport_dep_delay_trend pour l'aéroport {airport_code}:")
    print(response.json())
else:
    print(f"Erreur lors de l'appel de l'API airport_dep_delay_trend: {response.status_code}")

# Test de l'API airport_arr_delay_trend avec un code d'aéroport
response = requests.get(f"{base_url}/api/airport_arr_delay_trend", params={"airport_code": airport_code})
if response.status_code == 200:
    print(f"\nAPI airport_arr_delay_trend pour l'aéroport {airport_code}:")
    print(response.json())
else:
    print(f"Erreur lors de l'appel de l'API airport_arr_delay_trend: {response.status_code}")
