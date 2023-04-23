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
    origins = list(data['Origin'].unique())
    return jsonify(origins)


@app.route('/api/destinations', methods=['GET'])
def get_destinations():
    # Récupérer la liste des villes de destination
    destinations = list(data['Dest'].unique())
    return jsonify(destinations)


@app.route('/api/causes_delay', methods=['GET'])
def get_delay():
    # Récupérer les paramètres d'entrée depuis la requête HTTP
    origin = request.args.get('Origin')
    dest = request.args.get('Dest')

    # Filtrer les données selon les paramètres d'entrée
    filtered = data[(data['Origin'] == origin) & (data['Dest'] == dest)]

    # Calculer la médiane de retard par cause
    median_carrier_delay = filtered['CarrierDelay'].median()
    median_weather_delay = filtered['WeatherDelay'].median()
    median_nas_delay = filtered['NASDelay'].median()
    median_security_delay = filtered['SecurityDelay'].median()
    median_late_aircraft_delay = filtered['LateAircraftDelay'].median()

    # Créer un objet JSON avec les médianes de retard par cause
    result = {
        'CarrierDelay': median_carrier_delay,
        'WeatherDelay': median_weather_delay,
        'NASDelay': median_nas_delay,
        'SecurityDelay': median_security_delay,
        'LateAircraftDelay': median_late_aircraft_delay
    }

    # Renvoyer l'objet JSON en réponse à la requête HTTP
    return jsonify(result)
