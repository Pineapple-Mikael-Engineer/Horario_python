import json
import os
from datetime import date, timedelta

from .constants import DATA_FILE


def _sample_data():
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    registros = []
    temas = []
    tags = set()
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
        "settings": {"theme": "dark", "font_size": 13, "auto_registro_horario": True},
        "week_meta": {"start": monday.isoformat()},
    }


def load_data():
    defaults = _sample_data()
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            loaded = json.load(f)
        defaults.update({k: v for k, v in loaded.items() if k in defaults})
        defaults["settings"] = {**_sample_data()["settings"], **loaded.get("settings", {})}
        defaults["week_meta"] = {**_sample_data()["week_meta"], **loaded.get("week_meta", {})}

        today = date.today()
        current_monday = today - timedelta(days=today.weekday())
        if defaults["week_meta"].get("start") != current_monday.isoformat():
            defaults["schedule"] = {}
            defaults["week_meta"]["start"] = current_monday.isoformat()
        return normalize_data(defaults)
    return normalize_data(defaults)


def save_data(data):
    data = normalize_data(data)
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
    return normalize_data(defaults)


def normalize_data(data):
    data.setdefault("registros", [])
    data.setdefault("b1_temas", [])
    data.setdefault("tags", [])
    data.setdefault("schedule", {})
    data.setdefault("b_nombres", _sample_data()["b_nombres"])
    data.setdefault("settings", _sample_data()["settings"])
    data.setdefault("week_meta", _sample_data()["week_meta"])

    valid_blocks = {"B1", "B2", "B3", "B4", "EJ"}
    cleaned = []
    for r in data.get("registros", []):
        if not isinstance(r, dict):
            continue
        if r.get("bloque") not in valid_blocks:
            continue
        try:
            horas = float(r.get("horas", 0))
        except Exception:
            horas = 0.0
        if horas <= 0:
            continue
        cleaned.append({**r, "horas": horas, "tags": list(r.get("tags", []))})
    data["registros"] = cleaned
    data["tags"] = sorted(set(data.get("tags", [])), key=str.lower)
    return data
