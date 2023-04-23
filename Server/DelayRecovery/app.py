import sys

from flask import Blueprint
from pathlib import Path

from DataLoader.data_loader import DataLoader

app = Blueprint('Delay recovery', __name__)
sys.path.insert(0, str(Path(__file__).parent.parent))

# Charger les données de retard et les préparer pour l'analyse
data = DataLoader.data

