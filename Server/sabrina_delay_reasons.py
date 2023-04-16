import json
import pandas as pd
def analyze_flight_delays(year=None, quarter=None, month=None, day_of_month=None, day_of_week=None, reporting_airline=None, origin_city_name=None, dest_city_name=None):
    
    data = pd.read_csv('../ML/Datasets/DataFlightFinal.csv')

    # Filtrer le dataset en fonction des paramètres d'entrée
    filtered_data = data
    if year is not None:
        filtered_data = filtered_data[filtered_data['Year'] == year]
    if quarter is not None:
        filtered_data = filtered_data[filtered_data['Quarter'] == quarter]
    if month is not None:
        filtered_data = filtered_data[filtered_data['Month'] == month]
    if day_of_month is not None:
        filtered_data = filtered_data[filtered_data['DayofMonth'] == day_of_month]
    if day_of_week is not None:
        filtered_data = filtered_data[filtered_data['DayOfWeek'] == day_of_week]
    if reporting_airline is not None:
        filtered_data = filtered_data[filtered_data['Reporting_Airline'] == reporting_airline]
    if origin_city_name is not None:
        filtered_data = filtered_data[filtered_data['OriginCityName'] == origin_city_name]
    if dest_city_name is not None:
        filtered_data = filtered_data[filtered_data['DestCityName'] == dest_city_name]

    # Calculez les délais moyens pour chaque type de retard
    carrier_delay = filtered_data['CarrierDelay'].mean()
    weather_delay = filtered_data['WeatherDelay'].mean()
    nas_delay = filtered_data['NASDelay'].mean()
    security_delay = filtered_data['SecurityDelay'].mean()
    late_aircraft_delay = filtered_data['LateAircraftDelay'].mean()

    # Créez l'objet JSON à renvoyer
    result = {
        "CarrierDelay": carrier_delay,
        "WeatherDelay": weather_delay,
        "NASDelay": nas_delay,
        "SecurityDelay": security_delay,
        "LateAircraftDelay": late_aircraft_delay
    }
    
    return json.dumps(result)

def test_analyze_flight_delays() :

    # Exemple d'utilisation de la fonction avec des paramètres spécifiques
    resultat = analyze_flight_delays(year=2009, month=4, reporting_airline="WN")
    resultat_json = json.dumps(resultat, indent=2)

    print("Résultat avec des paramètres spécifiques:")
    print(resultat_json)

    # Exemple d'utilisation de la fonction sans paramètres (pour voir les moyennes générales)
    resultat_general = analyze_flight_delays()
    resultat_general_json = json.dumps(resultat_general, indent=2)

    print("\nRésultat sans paramètres (moyennes générales) :")
    print(resultat_general_json)

#test_analyze_flight_delays()
