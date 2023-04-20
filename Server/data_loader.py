import pandas as pd


class DataLoader:
    data = pd.read_csv('../ML/Datasets/DataFlightVersionFinal.csv')
    data = data[data["Year"] > 2014]
