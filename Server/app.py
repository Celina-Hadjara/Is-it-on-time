import pandas as pd
from flask import Flask, jsonify, request, url_for

app = Flask(__name__)

# Charger les données de retard et les préparer pour l'analyse
data = pd.read_csv('../ML/Datasets/DataFlightFinal.csv')

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

if __name__ == "__main__":
    app.run(debug=True)
