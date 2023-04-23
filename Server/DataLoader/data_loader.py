import os
import pandas as pd
from pathlib import Path


class DataLoader:
    # Trouver le chemin du répertoire contenant le fichier data_loader.py
    script_dir = Path(__file__).parent.absolute()

    # Créer le chemin absolu du fichier CSV en vous basant sur le répertoire de data_loader.py
    data_path = script_dir / '../../ML/Datasets/DataFlightVersionFinal.csv'

    # Charger les données à partir du fichier CSV
    data = pd.read_csv(data_path)
    data = data[data["Year"] > 2014]
