import os

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "productividad_data.json")

PALETTE = {
    "bg": "#08090c",
    "surface": "#0f1117",
    "surface2": "#161820",
    "surface3": "#1c1f2a",
    "border": "#1e2133",
    "text": "#dde1ec",
    "muted": "#5a6075",
    "dim": "#2a2d3a",
    "B1": "#a78bfa",
    "B2": "#38bdf8",
    "B3": "#2dd4bf",
    "B4": "#fb923c",
    "EJ": "#22c55e",
    "clase": "#818cf8",
}

BLOQUES = {
    "B1": ("Aprendizaje", PALETTE["B1"]),
    "B2": ("Proyectos", PALETTE["B2"]),
    "B3": ("Habilidades", PALETTE["B3"]),
    "B4": ("Otro", PALETTE["B4"]),
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
    "04–06": {d: ("EJ", "Ejercicio") for d in range(7)},
    "06–08": {d: ("MA", "Mañana") for d in range(7)},
    "08–09": {0: ("CLASE", "MC216"), 1: ("LIBRE", ""), 2: ("LIBRE", ""), 3: ("LIBRE", ""), 4: ("LIBRE", ""), 5: ("CLASE", "MT235"), 6: ("LIBRE", "")},
    "09–10": {0: ("CLASE", "MC216"), 1: ("LIBRE", ""), 2: ("LIBRE", ""), 3: ("LIBRE", ""), 4: ("LIBRE", ""), 5: ("CLASE", "MT235"), 6: ("LIBRE", "")},
    "10–11": {0: ("CLASE", "MC216"), 1: ("LIBRE", ""), 2: ("LIBRE", ""), 3: ("CLASE", "BRN01"), 4: ("CLASE", "MB536"), 5: ("LIBRE", ""), 6: ("LIBRE", "")},
    "11–12": {0: ("LIBRE", ""), 1: ("LIBRE", ""), 2: ("LIBRE", ""), 3: ("CLASE", "BRN01·ML140"), 4: ("CLASE", "MB536"), 5: ("CLASE", "BRN01"), 6: ("LIBRE", "")},
    "12–13": {0: ("LIBRE", ""), 1: ("LIBRE", ""), 2: ("LIBRE", ""), 3: ("CLASE", "BRN01·ML140"), 4: ("LIBRE", ""), 5: ("CLASE", "BRN01"), 6: ("LIBRE", "")},
    "13–14": {0: ("LIBRE", ""), 1: ("LIBRE", ""), 2: ("LIBRE", ""), 3: ("CLASE", "ML140"), 4: ("LIBRE", ""), 5: ("CLASE", "MC216"), 6: ("CLASE", "MC216")},
    "14–15": {0: ("LIBRE", ""), 1: ("LIBRE", ""), 2: ("LIBRE", ""), 3: ("LIBRE", ""), 4: ("LIBRE", ""), 5: ("CLASE", "MC216"), 6: ("CLASE", "MC216")},
    "15–16": {0: ("LIBRE", ""), 1: ("LIBRE", ""), 2: ("LIBRE", ""), 3: ("LIBRE", ""), 4: ("LIBRE", ""), 5: ("LIBRE", ""), 6: ("CLASE", "MC216")},
    "16–17": {0: ("CLASE", "ML140"), 1: ("LIBRE", ""), 2: ("CLASE", "MB536"), 3: ("CLASE", "ML140"), 4: ("LIBRE", ""), 5: ("LIBRE", ""), 6: ("LIBRE", "")},
    "17–18": {0: ("CLASE", "ML140"), 1: ("CENA", "Cena"), 2: ("CLASE", "MB536"), 3: ("CLASE", "ML140"), 4: ("LIBRE", ""), 5: ("LIBRE", ""), 6: ("LIBRE", "")},
    "18–19": {0: ("CENA", "Cena"), 1: ("CLASE", "MN121"), 2: ("CLASE", "MB536"), 3: ("CENA", "Cena"), 4: ("CENA", "Cena"), 5: ("LIBRE", ""), 6: ("LIBRE", "")},
    "19–20": {0: ("CLASE", "MN121"), 1: ("CLASE", "MN121"), 2: ("LIBRE", ""), 3: ("CLASE", "MT235"), 4: ("CLASE", "MN121"), 5: ("LIBRE", ""), 6: ("LIBRE", "")},
    "20–21": {0: ("CLASE", "MN121"), 1: ("CLASE", "MN121"), 2: ("LIBRE", ""), 3: ("CLASE", "MT235"), 4: ("CLASE", "MN121"), 5: ("LIBRE", ""), 6: ("LIBRE", "")},
    "21–22": {0: ("BL", "Lectura"), 1: ("CLASE", "MN121"), 2: ("BL", "Lectura"), 3: ("CLASE", "MT235"), 4: ("CLASE", "MN121"), 5: ("BL", "Lectura"), 6: ("BL", "Lectura")},
    "22–23": {d: ("BL", "Lectura") for d in range(7)},
}
