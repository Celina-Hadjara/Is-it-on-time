import sys

from flask import jsonify, request, Blueprint
from DataLoader.data_loader import DataLoader
from pathlib import Path

app = Blueprint('Airport', __name__)
sys.path.insert(0, str(Path(__file__).parent.parent))

# Charger les données de retard et les préparer pour l'analyse
data = DataLoader.data


def calculate_trend_data(airport_data, delay_col):
    grouped_data = airport_data.groupby(["Month"]).agg(
        mean_delay=(delay_col, "mean"),
        count_total=("Unique_Flight_ID", "count"),
        count_delayed=(delay_col, lambda x: x[x > 0].count()),
        count_cancelled=("Cancelled", "sum"),
        count_ontime=(delay_col, lambda x: x[x <= 0].count())
    )

    # Calculer les pourcentages
    grouped_data["pct_delayed"] = (grouped_data["count_delayed"] / grouped_data["count_total"]) * 100
    grouped_data["pct_cancelled"] = (grouped_data["count_cancelled"] / grouped_data["count_total"]) * 100
    grouped_data["pct_ontime"] = (grouped_data["count_ontime"] / grouped_data["count_total"]) * 100

    return grouped_data


@app.route("/api/airport_dep_list", methods=["GET"])
def airport_dep_list():
    airport_list = sorted(data["Origin"].unique())
    return jsonify({"airport_list": airport_list})


@app.route("/api/airport_dest_list", methods=["GET"])
def airport_dest_list():
    airport_list = sorted(data["Dest"].unique())
    return jsonify({"airport_list": airport_list})


@app.route("/api/airport_dep_delay_trend", methods=["GET"])
def airport_dep_delay_trend():
    airport_code = request.args.get("airport_code")
    if not airport_code:
        return jsonify({"error": "Paramètre 'airport_code' manquant"}), 400

    airport_data = data[data["Origin"] == airport_code]
    grouped_data = calculate_trend_data(airport_data, "DepDelayMinutes")

    # Préparer les données pour le JSON
    trend_data = {key: list(grouped_data[key]) for key in grouped_data.columns}
    trend_data["Month"] = list(grouped_data.index)

    return jsonify(trend_data)


@app.route("/api/airport_arr_delay_trend", methods=["GET"])
def airport_arr_delay_trend():
    airport_code = request.args.get("airport_code")
    if not airport_code:
        return jsonify({"error": "Paramètre 'airport_code' manquant"}), 400

    airport_data = data[data["Dest"] == airport_code]
    grouped_data = calculate_trend_data(airport_data, "ArrDelayMinutes")

    # Préparer les données pour le JSON
    trend_data = {key: list(grouped_data[key]) for key in grouped_data.columns}
    trend_data["Month"] = list(grouped_data.index)

    return jsonify(trend_data)