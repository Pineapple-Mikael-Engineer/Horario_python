import json
import os

from .constants import DATA_FILE


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "registros": [],
        "b1_temas": [],
        "tags": [],
        "schedule": {},
        "b_nombres": {"B1": "Aprendizaje", "B2": "Proyectos", "B3": "Habilidades", "B4": "Otro"},
    }


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
