import pandas as pd
from flask_cors import CORS
from flask import Flask, jsonify, request, url_for

app = Flask(__name__)
CORS(app)

# Charger les données de retard et les préparer pour l'analyse
data = pd.read_csv('../ML/Datasets/DataFlightFinal.csv')


@app.route("/api/airport_list", methods=["GET"])
def airport_list():
    airport_list = sorted(data["Origin"].unique())
    return jsonify({"airport_list": airport_list})


@app.route("/api/airport_delay_trend", methods=["GET"])
def airport_delay_trend():
    airport_code = request.args.get("airport_code")
    year = request.args.get("year")
    if not airport_code:
        return jsonify({"error": "Paramètre 'airport_code' manquant"}), 400
    if not year:
        return jsonify({"error": "Paramètre 'year' manquant"}), 400

    # Filtrer les données pour l'aéroport et l'année spécifiés
    airport_data = data[(data["Origin"] == airport_code) & (data["Year"] == int(year))]

    # Calculer les statistiques de retard
    grouped_data = airport_data.groupby(["Month"]).agg(
        mean_delay=("DepDelayMinutes", "mean"),
        count_total=("Flight_Number_Reporting_Airline", "count"),
        count_delayed=("DepDelayMinutes", lambda x: x[x > 0].count()),
        count_cancelled=("Cancelled", "sum"),
        count_ontime=("DepDelayMinutes", lambda x: x[x <= 0].count())
    )

    # Calculer les pourcentages
    grouped_data["pct_delayed"] = (grouped_data["count_delayed"] / grouped_data["count_total"]) * 100
    grouped_data["pct_cancelled"] = (grouped_data["count_cancelled"] / grouped_data["count_total"]) * 100
    grouped_data["pct_ontime"] = (grouped_data["count_ontime"] / grouped_data["count_total"]) * 100

    # Préparer les données pour le JSON
    trend_data = {
        "Month": list(grouped_data.index),
        "mean_delay": list(grouped_data["mean_delay"]),
        "count_total": list(grouped_data["count_total"]),
        "count_delayed": list(grouped_data["count_delayed"]),
        "count_cancelled": list(grouped_data["count_cancelled"]),
        "count_ontime": list(grouped_data["count_ontime"]),
        "pct_delayed": list(grouped_data["pct_delayed"]),
        "pct_cancelled": list(grouped_data["pct_cancelled"]),
        "pct_ontime": list(grouped_data["pct_ontime"])
    }

    # Renvoyer les données sous forme de JSON
    return jsonify(trend_data)


# ---Analyse par mois---#
@app.route("/api/delay_option_by_year", methods=["GET"])
def delay_option_by_year():
    year = request.args.get("year")
    option = request.args.get("option")
    option = option.title()

    if option == 'Dayofmonth':
        option = 'DayofMonth'
    elif option == 'Dayofweek':
        option = 'DayOfWeek'

    if not year:
        return jsonify({"error": "Paramètre 'year' manquant"}), 400
    if not option:
        return jsonify({"error": "Paramètre 'option' manquant"}), 400

    # Filtrer les données pour l'aéroport et l'année spécifiés
    airport_data = data[data["Year"] == int(year)]

    # Calculer les statistiques de retard
    grouped_data = airport_data.groupby([option]).agg(
        mean_delay=("DepDelayMinutes", "mean"),
        count_total=("Flight_Number_Reporting_Airline", "count"),
        count_delayed=("DepDelayMinutes", lambda x: x[x > 0].count()),
        count_ontime=("DepDelayMinutes", lambda x: x[x <= 0].count())
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
        "pct_ontime": list(grouped_data["pct_ontime"])
    }

    # Renvoyer les données sous forme de JSON
    return jsonify(trend_data)


@app.route("/api/calculate_delay_by_2hour", methods=["GET"])
def calculate_delay_by_2hour():
    year = request.args.get("year")

    if year != "total":
        airport_data = data[data["Year"] == int(year)]

    else:
        airport_data = data

    bins = pd.IntervalIndex.from_tuples([(i, i + 200) for i in range(0, 2400, 200)])

    # Categorize the values in the CRSArrTime column into hourly bins
    airport_data['hour_bin'] = pd.cut(airport_data['CRSArrTime'], bins)

    # Group the delayed flights by hour and count the number of delayed flights in each hour
    delay_counts = airport_data[airport_data['ArrDelayMinutes'] > 0].groupby('hour_bin')['ArrDelayMinutes'].count()

    # Convert the results to the desired format
    result = {
        "hour": [f"{int(b.left) / 100}h-{int(b.right) / 100}h" for b in delay_counts.index],
        "count_delayed": delay_counts.values.tolist()
    }

    return jsonify(result)


@app.route("/api/delay_by_day_month", methods=["GET"])
def delay_by_day_month():
    option1 = request.args.get("option1")
    option2 = request.args.get("option2")
    airport_depart = request.args.get("airport_depart")
    airport_arrive = request.args.get("airport_arrive")
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
    if not airport_depart:
        return jsonify({"error": "Paramètre 'airport_depart' manquant"}), 400
    if not airport_arrive:
        return jsonify({"error": "Paramètre 'airport_arrive' manquant"}), 400

    # Filtrer les données pour l'aéroport et l'année spécifiés
    airport_data = data[(data["Origin"] == airport_depart) & (data["Dest"] == airport_arrive) & (data["Year"] >= 2015)]
    # Calculer les statistiques de retard
    grouped_data = airport_data.groupby([option1, option2]).agg(
        mean_delay=("DepDelayMinutes", "mean"),
        count_total=("Flight_Number_Reporting_Airline", "count"),
        count_delayed=("DepDelayMinutes", lambda x: x[x > 0].count()),
        count_ontime=("DepDelayMinutes", lambda x: x[x <= 0].count())
    )

    result, option1_list, option2_list = delay_3dim(option1, option2, "DepDelayMinutes")


    # Calculer les pourcentages
    grouped_data["pct_delayed"] = (grouped_data["count_delayed"] / grouped_data["count_total"]) * 100
    grouped_data["pct_ontime"] = (grouped_data["count_ontime"] / grouped_data["count_total"]) * 100

    # Préparer les données pour le JSON
    trend_data = {
        option1: option1_list,
        option2: option2_list,
        "result": result.values.tolist(),
        "mean_delay": list(grouped_data["mean_delay"]),
        "count_total": list(grouped_data["count_total"]),
        "count_delayed": list(grouped_data["count_delayed"]),
        "count_ontime": list(grouped_data["count_ontime"]),
        "pct_delayed": list(grouped_data["pct_delayed"]),
        "pct_ontime": list(grouped_data["pct_ontime"])
    }

    # Renvoyer les données sous forme de JSON
    return jsonify(trend_data)


# change format data
def delay_3dim(index, colume, colume_value):
    month = data[colume].unique()
    n_data_per_heatmap = 40
    result = {}

    for i in range(0, len(month), n_data_per_heatmap):
        data1 = month[i:i + n_data_per_heatmap]

        pivot_df = pd.pivot_table(data[data[colume].isin(data1)], values=colume_value, index=[index], columns=[colume])

    return pivot_df, pivot_df.index.unique().tolist(), pivot_df.columns.tolist()



if __name__ == "__main__":
    app.run(debug=True)
