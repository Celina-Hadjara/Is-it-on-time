import sys

from flask import Blueprint, jsonify, request
from pathlib import Path
from DataLoader.data_loader import DataLoader

app = Blueprint('Delay reasons', __name__)
sys.path.insert(0, str(Path(__file__).parent.parent))

# Charger les données de retard et les préparer pour l'analyse
data = DataLoader.data


@app.route('/api/origins', methods=['GET'])
def get_origins():
    # Récupérer la liste des villes d'origine
    origins = list(data['OriginCityName'].unique())
    return jsonify(origins)


@app.route('/api/destinations', methods=['GET'])
def get_destinations():
    # Récupérer la liste des villes de destination
    destinations = list(data['DestCityName'].unique())
    return jsonify(destinations)


@app.route('/api/causes_delay', methods=['GET'])
def get_delay():
    # Récupérer les paramètres d'entrée depuis la requête HTTP
    origin_city = request.args.get('OriginCityName')
    dest_city = request.args.get('DestCityName')

    # Filtrer les données selon les paramètres d'entrée

    filtered = data[(data['OriginCityName'] == origin_city) & (data['DestCityName'] == dest_city)]

    #print(filtered)
    #print(origin_city)
    #print(dest_city)


    # Calculer la médiane de retard par cause
    mean_carrier_delay = filtered['CarrierDelay'].mean()
    mean_weather_delay = filtered['WeatherDelay'].mean()
    mean_nas_delay = filtered['NASDelay'].mean()
    mean_security_delay = filtered['SecurityDelay'].mean()
    mean_late_aircraft_delay = filtered['LateAircraftDelay'].mean()

    # Créer un objet JSON avec les médianes de retard par cause
    result = {
        'CarrierDelay': mean_carrier_delay,
        'WeatherDelay': mean_weather_delay,
        'NASDelay': mean_nas_delay,
        'SecurityDelay': mean_security_delay,
        'LateAircraftDelay': mean_late_aircraft_delay
    }

    # Renvoyer l'objet JSON en réponse à la requête HTTP
    return jsonify(result)

