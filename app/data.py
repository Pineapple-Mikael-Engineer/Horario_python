import json
import os
from datetime import date, timedelta

from .constants import DATA_FILE


def _sample_data():
    today = date.today()
    temas = [
        {"id": "py", "nombre": "Python"},
        {"id": "ia", "nombre": "IA aplicada"},
        {"id": "mate", "nombre": "Matemáticas"},
    ]
    tags = ["Programación", "Investigación", "Universidad", "Lectura", "Proyecto personal", "Salud"]

    registros = [
        {"date": (today - timedelta(days=10)).isoformat(), "bloque": "B1", "horas": 2.0, "nota": "Repaso de funciones y módulos", "subtema": "py", "tags": ["Programación", "Universidad"]},
        {"date": (today - timedelta(days=9)).isoformat(), "bloque": "B2", "horas": 1.5, "nota": "Avance de app de horarios", "subtema": None, "tags": ["Proyecto personal", "Programación"]},
        {"date": (today - timedelta(days=8)).isoformat(), "bloque": "EJ", "horas": 1.0, "nota": "Cardio + movilidad", "subtema": None, "tags": ["Salud"]},
        {"date": (today - timedelta(days=7)).isoformat(), "bloque": "B3", "horas": 1.0, "nota": "Lectura de documentación Qt", "subtema": None, "tags": ["Lectura", "Programación"]},
        {"date": (today - timedelta(days=6)).isoformat(), "bloque": "B1", "horas": 2.5, "nota": "Práctica de álgebra lineal", "subtema": "mate", "tags": ["Universidad"]},
        {"date": (today - timedelta(days=5)).isoformat(), "bloque": "B2", "horas": 2.0, "nota": "Diseño de dashboard", "subtema": None, "tags": ["Proyecto personal"]},
        {"date": (today - timedelta(days=4)).isoformat(), "bloque": "EJ", "horas": 1.0, "nota": "Rutina de fuerza", "subtema": None, "tags": ["Salud"]},
        {"date": (today - timedelta(days=3)).isoformat(), "bloque": "B1", "horas": 1.5, "nota": "Experimentos con embeddings", "subtema": "ia", "tags": ["Investigación", "Programación"]},
        {"date": (today - timedelta(days=2)).isoformat(), "bloque": "B4", "horas": 1.0, "nota": "Organización personal", "subtema": None, "tags": ["Proyecto personal"]},
        {"date": (today - timedelta(days=1)).isoformat(), "bloque": "B3", "horas": 1.5, "nota": "Práctica de mecanografía", "subtema": None, "tags": ["Salud"]},
    ]

    return {
        "registros": registros,
        "b1_temas": temas,
        "tags": sorted(tags, key=str.lower),
        "schedule": {},
        "b_nombres": {
            "B1": "Aprendizaje Teórico",
            "B2": "Práctica Dirigida",
            "B3": "Construcción / Proyecto",
            "B4": "Investigación / Debugging",
        },
    }


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return _sample_data()


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return _sample_data()


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def export_data(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def import_data(path):
    with open(path, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    defaults = _sample_data()
    defaults.update({k: v for k, v in loaded.items() if k in defaults})
    return defaults
