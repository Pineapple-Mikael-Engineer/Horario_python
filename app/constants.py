import os
import json

from .styles import get_palette

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "productividad_data.json")


def _resolve_theme_mode():
    env_mode = os.getenv("PRODUCTIVIDAD_THEME")
    if env_mode:
        return env_mode
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("settings", {}).get("theme", "dark")
        except Exception:
            return "dark"
    return "dark"


PALETTE = get_palette(_resolve_theme_mode())

BLOQUES = {
    "B1": ("Aprendizaje Teórico", PALETTE["B1"]),
    "B2": ("Práctica Dirigida", PALETTE["B2"]),
    "B3": ("Construcción / Proyecto", PALETTE["B3"]),
    "B4": ("Investigación / Debugging", PALETTE["B4"]),
    "EJ": ("Ejercicio", PALETTE["EJ"]),
}

DAYS_ES = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
HOURS = [
    "04–06", "06–08", "08–09", "09–10", "10–11", "11–12", "12–13",
    "13–14", "14–15", "15–16", "16–17", "17–18", "18–19", "19–20",
    "20–21", "21–22", "22–23",
]

SCHEDULE_TYPES = {
    "EJ": ("Ejercicio", PALETTE["EJ"]),
    "MA": ("Mañana", "#f97316"),
    "CLASE": ("Clase", PALETTE["clase"]),
    "LIBRE": ("Libre", PALETTE["dim"]),
    "CENA": ("Cena", "#fbbf24"),
    "BL": ("Lectura", PALETTE["B3"]),
    "B1": ("Bloque B1", PALETTE["B1"]),
    "B2": ("Bloque B2", PALETTE["B2"]),
    "B3": ("Bloque B3", PALETTE["B3"]),
    "B4": ("Bloque B4", PALETTE["B4"]),
}

BASE_SCHEDULE = {
    "04–06": {d: ("EJ", "🏃") for d in range(7)},
    "06–08": {d: ("MA", "🌅") for d in range(7)},
    "08–09": {0: ("CLASE", "🎓MC216"), 1: ("LIBRE", "🧠B*"), 2: ("LIBRE", "🧠B*"), 3: ("LIBRE", "🧠B*"), 4: ("LIBRE", "🧠B*"), 5: ("CLASE", "🎓MT235"), 6: ("LIBRE", "🧠B*")},
    "09–10": {0: ("CLASE", "🎓MC216"), 1: ("LIBRE", "🧠B*"), 2: ("LIBRE", "🧠B*"), 3: ("LIBRE", "🧠B*"), 4: ("LIBRE", "🧠B*"), 5: ("CLASE", "🎓MT235"), 6: ("LIBRE", "🧠B*")},
    "10–11": {0: ("CLASE", "🎓MC216"), 1: ("LIBRE", "🧠B*"), 2: ("LIBRE", "🧠B*"), 3: ("CLASE", "🎓BRN01"), 4: ("CLASE", "🎓MB536"), 5: ("LIBRE", "🧠B*"), 6: ("LIBRE", "🧠B*")},
    "11–12": {0: ("LIBRE", "🧠B*"), 1: ("LIBRE", "🧠B*"), 2: ("LIBRE", "🧠B*"), 3: ("CLASE", "🎓BRN01/🎓ML140"), 4: ("CLASE", "🎓MB536"), 5: ("CLASE", "🎓BRN01"), 6: ("LIBRE", "🧠B*")},
    "12–13": {0: ("LIBRE", "🧠B*"), 1: ("LIBRE", "🧠B*"), 2: ("LIBRE", "🧠B*"), 3: ("CLASE", "🎓BRN01/🎓ML140"), 4: ("LIBRE", "🧠B*"), 5: ("CLASE", "🎓BRN01"), 6: ("LIBRE", "🧠B*")},
    "13–14": {0: ("LIBRE", "🧠B*"), 1: ("LIBRE", "🧠B*"), 2: ("LIBRE", "🧠B*"), 3: ("CLASE", "🎓ML140"), 4: ("LIBRE", "🧠B*"), 5: ("CLASE", "🎓MC216"), 6: ("LIBRE", "🧠B*")},
    "14–15": {0: ("LIBRE", "🧠B*"), 1: ("LIBRE", "🧠B*"), 2: ("LIBRE", "🧠B*"), 3: ("LIBRE", "🧠B*"), 4: ("LIBRE", "🧠B*"), 5: ("CLASE", "🎓MC216"), 6: ("LIBRE", "🧠B*")},
    "15–16": {0: ("LIBRE", "🧠B*"), 1: ("LIBRE", "🧠B*"), 2: ("LIBRE", "🧠B*"), 3: ("LIBRE", "🧠B*"), 4: ("LIBRE", "🧠B*"), 5: ("CLASE", "🎓MC216"), 6: ("LIBRE", "🧠B*")},
    "16–17": {0: ("CLASE", "🎓ML140"), 1: ("LIBRE", "🧠B*"), 2: ("CLASE", "🎓MB536"), 3: ("CLASE", "🎓ML140"), 4: ("LIBRE", "🧠B*"), 5: ("LIBRE", "🧠B*"), 6: ("LIBRE", "🧠B*")},
    "17–18": {0: ("CLASE", "🎓ML140"), 1: ("CENA", "🍽"), 2: ("CLASE", "🎓MB536"), 3: ("CLASE", "🎓ML140"), 4: ("LIBRE", "🧠B*"), 5: ("LIBRE", "🧠B*"), 6: ("LIBRE", "🧠B*")},
    "18–19": {0: ("CENA", "🍽"), 1: ("CLASE", "🎓MN121"), 2: ("CLASE", "🎓MB536"), 3: ("CENA", "🍽"), 4: ("CENA", "🍽"), 5: ("LIBRE", "🧠B*"), 6: ("LIBRE", "🧠B*")},
    "19–20": {0: ("CLASE", "🎓MN121"), 1: ("CLASE", "🎓MN121"), 2: ("LIBRE", "🧠B*"), 3: ("CLASE", "🎓MT235"), 4: ("CLASE", "🎓MN121"), 5: ("LIBRE", "🧠B*"), 6: ("LIBRE", "🧠B*")},
    "20–21": {0: ("CLASE", "🎓MN121"), 1: ("CLASE", "🎓MN121"), 2: ("LIBRE", "🧠B*"), 3: ("CLASE", "🎓MT235"), 4: ("CLASE", "🎓MN121"), 5: ("LIBRE", "🧠B*"), 6: ("LIBRE", "🧠B*")},
    "21–22": {0: ("BL", "📗BL"), 1: ("CLASE", "🎓MN121"), 2: ("BL", "📗BL"), 3: ("CLASE", "🎓MT235"), 4: ("CLASE", "🎓MN121"), 5: ("BL", "📗BL"), 6: ("BL", "📗BL")},
    "22–23": {d: ("BL", "📗BL") for d in range(7)},
}
