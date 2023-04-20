import pandas as pd
from flask_cors import CORS
from flask import Flask, jsonify, request, url_for

app = Flask(__name__)
CORS(app)

# Charger les données de retard et les préparer pour l'analyse
data = pd.read_csv('../ML/Datasets/DataFlightVersionFinal.csv')

@app.route("/api/airport_list", methods=["GET"])
def airport_list():
    airport_list = sorted(data["Origin"].unique())
    return jsonify({"airport_list": airport_list})

@app.route("/api/year_list", methods=["GET"])
def year_list():
    airport_code = request.args.get("airport_code")
    if not airport_code:
        return jsonify({"error": "Paramètre 'airport_code' manquant"}), 400

    # Filtrer les données pour l'aéroport spécifié et extraire les années
    airport_data = data[data["Origin"] == airport_code]
    year_list = sorted(airport_data["Year"].unique())

    # Convertir les entiers int64 en int
    year_list = [int(year) for year in year_list]

    # Renvoyer la liste des années sous forme de JSON
    return jsonify({"year_list": year_list})

@app.route("/api/airport_delay_trend", methods=["GET"])
def airport_delay_trend():
    airport_code = request.args.get("airport_code")
    year = request.args.get("year")  # Modification ici
    if not airport_code:
        return jsonify({"error": "Paramètre 'airport_code' manquant"}), 400
    if not year:
        return jsonify({"error": "Paramètre 'year' manquant"}), 400

    # Filtrer les données pour l'aéroport et l'année spécifiés et calculer les statistiques de retard
    airport_data = data[(data["Origin"] == airport_code) & (data["Year"] == int(year))]
    grouped_data = airport_data.groupby(["Month"]).agg({"ArrDelayMinutes": "mean"})
    trend_data = {"Month": list(grouped_data.index), "mean_delay": list(grouped_data["ArrDelayMinutes"])}

    # Renvoyer les données sous forme de JSON
    return jsonify(trend_data)


#########################################################
############## API Companies ############################
#########################################################

@app.route("/api/list_state", methods=["GET"])
def list_state():
    trend_data = data["OriginStateName"].unique().tolist()
    trend_data.sort()
    return trend_data

@app.route("/api/list_city", methods=["GET"])
def list_city():
    trend_data = data["DestCityName"].unique().tolist()
    trend_data.sort()
    return trend_data
@app.route("/api/list_code_companies", methods=["GET"])
def list_code_companies():
    trend_data = data["Reporting_Airline"].unique().tolist()
    trend_data.sort()
    return trend_data


@app.route("/api/companie_delay_compa", methods=["GET"])
def companie_delay_compa():

    # Filtrer les données pour la companie et l'année spécifiés et calculer les statistiques de retard
    companies_data = data[((data["Year"] <= 2015))]
    grouped_data = companies_data.groupby(["Reporting_Airline"]).agg({"ArrDelayMinutes": "mean"})
    trend_data = {"Reporting_Airline": list(grouped_data.index), "mean_delay": list(grouped_data["ArrDelayMinutes"])}

    # Renvoyer les données sous forme de JSON
    return jsonify(trend_data)


@app.route("/api/companie_delay_trend", methods=["GET"])
def companie_delay_trend():
    companie_code = request.args.get("companie_code")
    if not companie_code:
        return jsonify({"error": "Paramètre 'companie_code' manquant"}), 400

    # Filtrer les données pour la companie et l'année spécifiés et calculer les statistiques de retard
    companies_data = data[(data["Reporting_Airline"] == companie_code) & (data["Year"] <= 2015)]
    grouped_data = companies_data.groupby(["Month"]).agg({"ArrDelayMinutes": "mean"})
    trend_data = {"Month": list(grouped_data.index), "mean_delay": list(grouped_data["ArrDelayMinutes"])}

    # Renvoyer les données sous forme de JSON
    return jsonify(trend_data)

@app.route("/api/companie_cancelled", methods=["GET"])
def companie_cancelled():
    companie_code = request.args.get("companie_code")

    if not companie_code:
        return jsonify({"error": "Paramètre 'companie_code' manquant"}), 400


    # Filtrer les données pour la companie et l'année spécifiés et calculer le nombre de vols annulés
    companies_data = data[(data["Reporting_Airline"] == companie_code) & (data["Year"] <= 2015)]
    grouped_data = companies_data.groupby(["Month"]).agg({"Cancelled": "sum" , "Flight_Number_Reporting_Airline": "count"})
    cancelled_data = {"Month": list(grouped_data.index), "sum_cancelled": list(grouped_data["Cancelled"]) ,"count_flights": list(grouped_data["Flight_Number_Reporting_Airline"]) }
    # Renvoyer les données sous forme de JSON
    return jsonify(cancelled_data)


@app.route("/api/state_delay_trend", methods=["GET"])
def state_delay_trend():
    state_origin_name = request.args.get("state_origin_name")
    state_dest_name = request.args.get("state_dest_name")

    if not state_origin_name:
        return jsonify({"error": "Paramètre 'state_origin_name' manquant"}), 400
    if not state_dest_name:
        return jsonify({"error": "Paramètre 'state_dest_name' manquant"}), 400


    # Filtrer les données pour les etats(origin --> dest) et l'année spécifiés et calculer les statistiques de retard
    companies_data = data[(data["OriginStateName"] == state_origin_name) & (data["DestStateName"] == state_dest_name) & (data["Year"] <= 2015)]
    grouped_data = companies_data.groupby(["Month"]).agg({"ArrDelayMinutes": "mean"})
    trend_data = {"Month": list(grouped_data.index), "mean_delay": list(grouped_data["ArrDelayMinutes"])}

    # Renvoyer les données sous forme de JSON
    return jsonify(trend_data)


@app.route("/api/city_delay_trend", methods=["GET"])
def city_delay_trend():
    originCityName = request.args.get("originCityName")
    destCityName = request.args.get("destCityName")
    year = request.args.get("year")
    if not originCityName:
        return jsonify({"error": "Paramètre 'OriginCityName' manquant"}), 400
    if not destCityName:
        return jsonify({"error": "Paramètre 'destCityName' manquant"}), 400


    # Filtrer les données pour les etats(origin --> dest) et l'année spécifiés et calculer les statistiques de retard
    companies_data = data[(data["OriginCityName"] == originCityName) & (data["DestCityName"] == destCityName) & (data["Year"] <= 2015 )]
    grouped_data = companies_data.groupby(["Month"]).agg({"ArrDelayMinutes": "mean"})
    trend_data = {"Month": list(grouped_data.index), "mean_delay": list(grouped_data["ArrDelayMinutes"])}

    # Renvoyer les données sous forme de JSON
    return jsonify(trend_data)

if __name__ == "__main__":
    app.run(debug=True)
