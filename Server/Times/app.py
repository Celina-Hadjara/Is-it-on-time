import sys

from flask import Blueprint, jsonify, request
from pathlib import Path

from DataLoader.data_loader import DataLoader

app = Blueprint('Times', __name__)
sys.path.insert(0, str(Path(__file__).parent.parent))

# Charger les données de retard et les préparer pour l'analyse
data = DataLoader.data


#########################################################
############## API Times ############################
#########################################################

# ---Analyse par mois---#
@app.route("/api/delay_option_by_year", methods=["GET"])
def delay_option_by_year():
    option = request.args.get("option")
    option = option.title()
    code_state_origin = request.args.get("codeStateOrigin")
    code_state_dest = request.args.get("codeStateDest")

    if option == 'Dayofmonth':
        option = 'DayofMonth'
    elif option == 'Dayofweek':
        option = 'DayOfWeek'
    if not option:
        return jsonify({"error": "Paramètre 'option' manquant"}), 400
    if not code_state_origin:
        return jsonify({"error": "Paramètre 'codeStateOrigin' manquant"}), 400
    if not code_state_dest:
        return jsonify({"error": "Paramètre 'codeStateDest' manquant"}), 400

    # Filtrer les données pour l'aéroport et l'année spécifiés
    airport_data = data[
        (data["OriginStateName"] == code_state_origin) & (data["DestStateName"] == code_state_dest) & (
                data["Year"] >= 2015)]

    # Calculer les statistiques de retard
    grouped_data = airport_data[airport_data['DepDelayMinutes'] > 0].groupby([option]).agg(
        mean_delay=("DepDelayMinutes", "mean"),
        count_total=("Flight_Number_Reporting_Airline", "count"),
        count_delayed=("DepDelayMinutes", lambda x: x[x > 0].count()),
        count_ontime=("DepDelayMinutes", lambda x: x[x <= 0].count()),
        highest_delay=("DepDelayMinutes", "max"),
        lowest_delay=("DepDelayMinutes", "min")
    )

    # Calculer les pourcentages
    grouped_data["pct_delayed"] = (grouped_data["count_delayed"] / grouped_data["count_total"]) * 100
    grouped_data["pct_ontime"] = (grouped_data["count_ontime"] / grouped_data["count_total"]) * 100

    # Préparer les données pour le JSON
    trend_data = {
        option: list(grouped_data.index),
        "mean_delay": list(grouped_data["mean_delay"]),
        "count_total": list(grouped_data["count_total"]),
        "count_delayed": list(grouped_data["count_delayed"]),
        "count_ontime": list(grouped_data["count_ontime"]),
        "pct_delayed": list(grouped_data["pct_delayed"]),
        "pct_ontime": list(grouped_data["pct_ontime"]),
        "highest_delay": list(grouped_data["highest_delay"]),
        "lowest_delay": list(grouped_data["lowest_delay"])
    }

    # Renvoyer les données sous forme de JSON
    return jsonify(trend_data)


@app.route("/api/calculate_delay_by_2hour", methods=["GET"])
def calculate_delay_by_2hour():
    code_state_origin = request.args.get("codeStateOrigin")
    code_state_dest = request.args.get("codeStateDest")
    hour = request.args.get("hour")

    if not code_state_origin:
        return jsonify({"error": "Paramètre 'codeStateOrigin' manquant"}), 400
    if not code_state_dest:
        return jsonify({"error": "Paramètre 'codeStateDest' manquant"}), 400
    if not hour:
        return jsonify({"error": "Paramètre 'hour' manquant"}), 400

    # Filtrer les données pour l'aéroport et l'année spécifiés
    airport_data = data[
        (data["OriginStateName"] == code_state_origin) & (data["DestStateName"] == code_state_dest) & (
                data["Year"] >= 2015)]
    if hour == "2h":
        bins = pd.IntervalIndex.from_tuples([(i, i + 200) for i in range(0, 2400, 200)])
    elif hour == "4h":
        bins = pd.IntervalIndex.from_tuples([(i, i + 400) for i in range(0, 2400, 400)])
    else:
        bins = pd.IntervalIndex.from_tuples([(i, i + 600) for i in range(0, 2400, 600)])

    # Categorize the values in the CRSArrTime column into hourly bins
    airport_data['hour_bin'] = pd.cut(airport_data['CRSArrTime'], bins)

    # Group the delayed flights by hour and count the number of delayed flights in each hour
    delay_counts = airport_data[airport_data['DepDelayMinutes'] > 0].groupby('hour_bin')['DepDelayMinutes'].agg(['mean', 'max',"min"])

    # Convert the results to the desired format
    result = {
        "hour": [f"{int(b.left) / 100}h-{int(b.right) / 100}h" for b in delay_counts.index],
        "count_delayed": delay_counts['mean'].fillna(0).values.tolist(),
        "max_delayed": delay_counts['max'].fillna(0).values.tolist(),
        "min_delayed": delay_counts['min'].fillna(0).values.tolist()
    }

    return jsonify(result)


@app.route("/api/delay_by_day_month", methods=["GET"])
def delay_by_day_month():
    option1 = request.args.get("option1")
    option2 = request.args.get("option2")
    ville_depart = request.args.get("ville_depart")
    ville_arrive = request.args.get("ville_arrive")
    option1 = option1.title()
    option2 = option2.title()

    if option1 == 'Dayofmonth':
        option1 = 'DayofMonth'
    elif option1 == 'Dayofweek':
        option1 = 'DayOfWeek'

    if option2 == 'Dayofmonth':
        option2 = 'DayofMonth'
    elif option2 == 'Dayofweek':
        option2 = 'DayOfWeek'

    if not option1:
        return jsonify({"error": "Paramètre 'option1' manquant"}), 400
    if not option2:
        return jsonify({"error": "Paramètre 'option2' manquant"}), 400
    if not ville_depart:
        return jsonify({"error": "Paramètre 'airport_depart' manquant"}), 400
    if not ville_arrive:
        return jsonify({"error": "Paramètre 'airport_arrive' manquant"}), 400

    # Filtrer les données pour l'aéroport et l'année spécifiés
    airport_data = data[
        (data["OriginStateName"] == ville_depart) & (data["DestStateName"] == ville_arrive)]
    result = delay_3dim(airport_data, option1, option2, "ArrDelayMinutes")
    option1_list = sorted(data[option1].unique().tolist())
    option2_list = sorted(data[option2].unique().tolist())
    # Préparer les données pour le JSON
    trend_data = {
        option1: option1_list,
        option2: option2_list,
        "result": result.values.tolist(),
    }

    # Renvoyer les données sous forme de JSON
    return jsonify(trend_data)


# change format data
def delay_3dim(dataset, index, colume, colume_value):
    month = dataset[colume].unique()
    n_data_per_heatmap = 40
    pivot_df = pd.DataFrame()
    for i in range(0, len(month), n_data_per_heatmap):
        data1 = month[i:i + n_data_per_heatmap]

        pivot_df = pd.pivot_table(dataset[dataset[colume].isin(data1)], values=colume_value, index=[index],
                                  columns=[colume]).fillna(0)

    return pivot_df


