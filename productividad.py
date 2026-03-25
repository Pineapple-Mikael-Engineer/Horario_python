"""
╔══════════════════════════════════════════════════════════╗
║          PANEL DE PRODUCTIVIDAD — PyQt6 + JSON           ║
║  Instalar: pip install PyQt6 matplotlib                  ║
║  Ejecutar: python productividad.py                       ║
╚══════════════════════════════════════════════════════════╝
"""

import sys, json, os
from datetime import date, datetime, timedelta
from collections import defaultdict

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QComboBox, QDoubleSpinBox,
    QLineEdit, QListWidget, QListWidgetItem, QDialog, QDialogButtonBox,
    QTabWidget, QScrollArea, QFrame, QSizePolicy, QMessageBox,
    QStackedWidget, QSpinBox, QTextEdit, QSplitter, QGroupBox,
    QCheckBox
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QDate
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon

import matplotlib
matplotlib.use("QtAgg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
#  CONSTANTES Y PALETA
# ─────────────────────────────────────────────────────────────────────────────
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "productividad_data.json")

PALETTE = {
    "bg":       "#08090c",
    "surface":  "#0f1117",
    "surface2": "#161820",
    "surface3": "#1c1f2a",
    "border":   "#1e2133",
    "text":     "#dde1ec",
    "muted":    "#5a6075",
    "dim":      "#2a2d3a",
    "B1":       "#a78bfa",   # violeta — aprendizaje
    "B2":       "#38bdf8",   # sky     — proyectos
    "B3":       "#2dd4bf",   # teal    — habilidades
    "B4":       "#fb923c",   # amber   — otro
    "EJ":       "#22c55e",   # verde   — ejercicio
    "clase":    "#818cf8",
}

BLOQUES = {
    "B1": ("Aprendizaje",  PALETTE["B1"]),
    "B2": ("Proyectos",    PALETTE["B2"]),
    "B3": ("Habilidades",  PALETTE["B3"]),
    "B4": ("Otro",         PALETTE["B4"]),
    "EJ": ("Ejercicio",    PALETTE["EJ"]),
}

DAYS_ES  = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
HOURS    = ["04–06","06–08","08–09","09–10","10–11","11–12","12–13",
            "13–14","14–15","15–16","16–17","17–18","18–19","19–20",
            "20–21","21–22","22–23"]

SCHEDULE_TYPES = {
    "EJ":    ("Ejercicio",       PALETTE["EJ"]),
    "MA":    ("Mañana",          "#f97316"),
    "CLASE": ("Clase",           PALETTE["clase"]),
    "LIBRE": ("Libre",           PALETTE["dim"]),
    "CENA":  ("Cena",            "#fbbf24"),
    "BL":    ("Lectura",         PALETTE["B3"]),
    "B1":    ("Bloque B1",       PALETTE["B1"]),
    "B2":    ("Bloque B2",       PALETTE["B2"]),
    "B3":    ("Bloque B3",       PALETTE["B3"]),
    "B4":    ("Bloque B4",       PALETTE["B4"]),
}

# Horario base (tipo, texto)
BASE_SCHEDULE = {
    "04–06": {d: ("EJ","Ejercicio") for d in range(7)},
    "06–08": {d: ("MA","Mañana")    for d in range(7)},
    "08–09": {0:("CLASE","MC216"),1:("LIBRE",""),2:("LIBRE",""),3:("LIBRE",""),
              4:("LIBRE",""),5:("CLASE","MT235"),6:("LIBRE","")},
    "09–10": {0:("CLASE","MC216"),1:("LIBRE",""),2:("LIBRE",""),3:("LIBRE",""),
              4:("LIBRE",""),5:("CLASE","MT235"),6:("LIBRE","")},
    "10–11": {0:("CLASE","MC216"),1:("LIBRE",""),2:("LIBRE",""),3:("CLASE","BRN01"),
              4:("CLASE","MB536"),5:("LIBRE",""),6:("LIBRE","")},
    "11–12": {0:("LIBRE",""),1:("LIBRE",""),2:("LIBRE",""),3:("CLASE","BRN01·ML140"),
              4:("CLASE","MB536"),5:("CLASE","BRN01"),6:("LIBRE","")},
    "12–13": {0:("LIBRE",""),1:("LIBRE",""),2:("LIBRE",""),3:("CLASE","BRN01·ML140"),
              4:("LIBRE",""),5:("CLASE","BRN01"),6:("LIBRE","")},
    "13–14": {0:("LIBRE",""),1:("LIBRE",""),2:("LIBRE",""),3:("CLASE","ML140"),
              4:("LIBRE",""),5:("CLASE","MC216"),6:("CLASE","MC216")},
    "14–15": {0:("LIBRE",""),1:("LIBRE",""),2:("LIBRE",""),3:("LIBRE",""),
              4:("LIBRE",""),5:("CLASE","MC216"),6:("CLASE","MC216")},
    "15–16": {0:("LIBRE",""),1:("LIBRE",""),2:("LIBRE",""),3:("LIBRE",""),
              4:("LIBRE",""),5:("LIBRE",""),6:("CLASE","MC216")},
    "16–17": {0:("CLASE","ML140"),1:("LIBRE",""),2:("CLASE","MB536"),3:("CLASE","ML140"),
              4:("LIBRE",""),5:("LIBRE",""),6:("LIBRE","")},
    "17–18": {0:("CLASE","ML140"),1:("CENA","Cena"),2:("CLASE","MB536"),3:("CLASE","ML140"),
              4:("LIBRE",""),5:("LIBRE",""),6:("LIBRE","")},
    "18–19": {0:("CENA","Cena"),1:("CLASE","MN121"),2:("CLASE","MB536"),3:("CENA","Cena"),
              4:("CENA","Cena"),5:("LIBRE",""),6:("LIBRE","")},
    "19–20": {0:("CLASE","MN121"),1:("CLASE","MN121"),2:("LIBRE",""),3:("CLASE","MT235"),
              4:("CLASE","MN121"),5:("LIBRE",""),6:("LIBRE","")},
    "20–21": {0:("CLASE","MN121"),1:("CLASE","MN121"),2:("LIBRE",""),3:("CLASE","MT235"),
              4:("CLASE","MN121"),5:("LIBRE",""),6:("LIBRE","")},
    "21–22": {0:("BL","Lectura"),1:("CLASE","MN121"),2:("BL","Lectura"),3:("CLASE","MT235"),
              4:("CLASE","MN121"),5:("BL","Lectura"),6:("BL","Lectura")},
    "22–23": {d:("BL","Lectura") for d in range(7)},
}

# ─────────────────────────────────────────────────────────────────────────────
#  DATOS
# ─────────────────────────────────────────────────────────────────────────────
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "registros": [],       # [{date, bloque, horas, subtema, nota}]
        "b1_temas":  [],       # [{id, nombre, color}]
        "schedule":  {},       # {hora: {day_idx: [tipo, texto]}}
        "b_nombres": {         # nombres personalizables de bloques
            "B1":"Aprendizaje","B2":"Proyectos","B3":"Habilidades","B4":"Otro"
        },
    }

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ─────────────────────────────────────────────────────────────────────────────
#  ESTILOS
# ─────────────────────────────────────────────────────────────────────────────
GLOBAL_STYLE = f"""
QMainWindow, QWidget {{
    background: {PALETTE['bg']};
    color: {PALETTE['text']};
    font-family: 'Segoe UI', 'Ubuntu', sans-serif;
    font-size: 13px;
}}
QTabWidget::pane {{ border: 1px solid {PALETTE['border']}; background: {PALETTE['surface']}; border-radius: 8px; }}
QTabBar::tab {{
    background: {PALETTE['surface2']}; color: {PALETTE['muted']};
    padding: 10px 22px; border-radius: 6px; margin-right: 4px;
    font-weight: 500; font-size: 13px;
}}
QTabBar::tab:selected {{ background: {PALETTE['surface3']}; color: {PALETTE['text']}; }}
QTabBar::tab:hover {{ color: {PALETTE['text']}; }}
QPushButton {{
    background: {PALETTE['surface2']}; color: {PALETTE['text']};
    border: 1px solid {PALETTE['border']}; border-radius: 8px;
    padding: 8px 18px; font-size: 13px; font-weight: 500;
}}
QPushButton:hover {{ background: {PALETTE['surface3']}; border-color: #2e3350; }}
QPushButton:pressed {{ background: {PALETTE['dim']}; }}
QLineEdit, QTextEdit, QDoubleSpinBox, QSpinBox, QComboBox {{
    background: {PALETTE['surface2']}; color: {PALETTE['text']};
    border: 1px solid {PALETTE['border']}; border-radius: 7px;
    padding: 7px 11px; font-size: 13px;
    selection-background-color: {PALETTE['B1']};
}}
QComboBox::drop-down {{ border: none; width: 20px; }}
QComboBox QAbstractItemView {{
    background: {PALETTE['surface2']}; color: {PALETTE['text']};
    border: 1px solid {PALETTE['border']}; selection-background-color: {PALETTE['surface3']};
}}
QListWidget {{
    background: {PALETTE['surface']}; color: {PALETTE['text']};
    border: 1px solid {PALETTE['border']}; border-radius: 8px; padding: 4px;
}}
QListWidget::item {{ padding: 7px 10px; border-radius: 5px; }}
QListWidget::item:selected {{ background: {PALETTE['surface3']}; color: {PALETTE['text']}; }}
QListWidget::item:hover {{ background: {PALETTE['surface2']}; }}
QScrollBar:vertical {{ background: {PALETTE['bg']}; width: 6px; }}
QScrollBar::handle:vertical {{ background: {PALETTE['border']}; border-radius: 3px; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
QGroupBox {{
    border: 1px solid {PALETTE['border']}; border-radius: 10px;
    margin-top: 14px; padding: 12px; color: {PALETTE['muted']}; font-size: 12px;
}}
QGroupBox::title {{ subcontrol-origin: margin; left: 12px; padding: 0 6px; }}
QSplitter::handle {{ background: {PALETTE['border']}; }}
"""

def btn_color(color, text_color="#ffffff"):
    return f"""
        QPushButton {{
            background: {color}22; color: {color};
            border: 1px solid {color}55; border-radius: 8px;
            padding: 8px 16px; font-weight: 600;
        }}
        QPushButton:hover {{ background: {color}44; }}
        QPushButton:pressed {{ background: {color}66; }}
    """

def card_style(accent=None):
    border = f"1px solid {accent}44" if accent else f"1px solid {PALETTE['border']}"
    return f"""
        QFrame {{
            background: {PALETTE['surface']}; border: {border};
            border-radius: 12px; padding: 4px;
        }}
    """

# ─────────────────────────────────────────────────────────────────────────────
#  WIDGETS REUTILIZABLES
# ─────────────────────────────────────────────────────────────────────────────
class Separator(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameShape(QFrame.Shape.HLine)
        self.setStyleSheet(f"background: {PALETTE['border']}; max-height: 1px; border: none;")

class Label(QLabel):
    def __init__(self, text, size=13, color=None, bold=False, italic=False):
        super().__init__(text)
        c = color or PALETTE['text']
        w = "700" if bold else "400"
        style = f"color:{c}; font-size:{size}px; font-weight:{w};"
        if italic: style += "font-style:italic;"
        self.setStyleSheet(style)
        self.setWordWrap(True)

class KpiCard(QFrame):
    def __init__(self, label, value, color, sub=""):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background: {PALETTE['surface']};
                border: 1px solid {color}33;
                border-left: 3px solid {color};
                border-radius: 10px; padding: 2px;
            }}
        """)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16,14,16,14)
        lay.setSpacing(4)
        lay.addWidget(Label(label, 11, PALETTE['muted']))
        self.val_lbl = Label(value, 26, color, bold=True)
        lay.addWidget(self.val_lbl)
        if sub:
            lay.addWidget(Label(sub, 11, PALETTE['muted']))

    def update_value(self, v):
        self.val_lbl.setText(v)

class MplCanvas(FigureCanvas):
    def __init__(self, w=6, h=3.5):
        self.fig = Figure(figsize=(w, h), facecolor=PALETTE['surface'])
        super().__init__(self.fig)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

# ─────────────────────────────────────────────────────────────────────────────
#  DIÁLOGO: REGISTRAR BLOQUE
# ─────────────────────────────────────────────────────────────────────────────
class RegistrarDialog(QDialog):
    def __init__(self, data, bloque_default=None, parent=None):
        super().__init__(parent)
        self.data = data
        self.setWindowTitle("Registrar sesión")
        self.setMinimumWidth(420)
        self.setStyleSheet(GLOBAL_STYLE + f"""
            QDialog {{ background:{PALETTE['surface2']}; border-radius:14px; }}
        """)

        lay = QVBoxLayout(self)
        lay.setSpacing(14)
        lay.setContentsMargins(24,24,24,24)

        lay.addWidget(Label("Registrar sesión", 17, bold=True))
        lay.addWidget(Separator())

        # Fecha
        row_f = QHBoxLayout()
        row_f.addWidget(Label("Fecha:", 13, PALETTE['muted']))
        self.fecha_edit = QLineEdit(str(date.today()))
        self.fecha_edit.setPlaceholderText("YYYY-MM-DD")
        row_f.addWidget(self.fecha_edit)
        lay.addLayout(row_f)

        # Bloque
        row_b = QHBoxLayout()
        row_b.addWidget(Label("Bloque:", 13, PALETTE['muted']))
        self.bloque_cb = QComboBox()
        bnames = data.get("b_nombres", {})
        for k, (default_name, color) in BLOQUES.items():
            name = bnames.get(k, default_name) if k != "EJ" else "Ejercicio"
            self.bloque_cb.addItem(f"{k} — {name}", k)
        if bloque_default:
            idx = [self.bloque_cb.itemData(i) for i in range(self.bloque_cb.count())].index(bloque_default)
            self.bloque_cb.setCurrentIndex(idx)
        row_b.addWidget(self.bloque_cb)
        lay.addLayout(row_b)
        self.bloque_cb.currentIndexChanged.connect(self._on_bloque_change)

        # Horas
        row_h = QHBoxLayout()
        row_h.addWidget(Label("Horas:", 13, PALETTE['muted']))
        self.horas_spin = QDoubleSpinBox()
        self.horas_spin.setRange(0.25, 12.0)
        self.horas_spin.setSingleStep(0.25)
        self.horas_spin.setValue(1.0)
        self.horas_spin.setSuffix(" h")
        row_h.addWidget(self.horas_spin)
        lay.addLayout(row_h)

        # Subtema B1
        self.b1_frame = QGroupBox("Subtema de aprendizaje (B1)")
        b1_lay = QVBoxLayout(self.b1_frame)
        self.tema_cb = QComboBox()
        self._reload_temas()
        b1_lay.addWidget(self.tema_cb)
        lay.addWidget(self.b1_frame)

        # Nota
        self.nota_edit = QLineEdit()
        self.nota_edit.setPlaceholderText("Nota opcional (¿qué trabajaste?)")
        lay.addWidget(self.nota_edit)

        lay.addWidget(Separator())
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.button(QDialogButtonBox.StandardButton.Ok).setText("Guardar")
        btns.button(QDialogButtonBox.StandardButton.Cancel).setText("Cancelar")
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        lay.addWidget(btns)

        self._on_bloque_change()

    def _reload_temas(self):
        self.tema_cb.clear()
        for t in self.data.get("b1_temas", []):
            self.tema_cb.addItem(t["nombre"], t["id"])

    def _on_bloque_change(self):
        self.b1_frame.setVisible(self.bloque_cb.currentData() == "B1")

    def get_registro(self):
        return {
            "date":   self.fecha_edit.text().strip(),
            "bloque": self.bloque_cb.currentData(),
            "horas":  self.horas_spin.value(),
            "subtema": self.tema_cb.currentData() if self.bloque_cb.currentData()=="B1" else None,
            "nota":   self.nota_edit.text().strip(),
        }

# ─────────────────────────────────────────────────────────────────────────────
#  DIÁLOGO: ADMINISTRAR TEMAS B1
# ─────────────────────────────────────────────────────────────────────────────
class TemasB1Dialog(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.setWindowTitle("Administrar temas B1")
        self.setMinimumSize(400, 420)
        self.setStyleSheet(GLOBAL_STYLE)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(20,20,20,20)
        lay.setSpacing(12)
        lay.addWidget(Label("Temas de Aprendizaje (B1)", 16, bold=True))
        lay.addWidget(Label("Define los subtemas y lleva el tiempo por cada uno.", 12, PALETTE['muted']))
        lay.addWidget(Separator())

        self.list_w = QListWidget()
        self._reload()
        lay.addWidget(self.list_w)

        row = QHBoxLayout()
        self.new_name = QLineEdit()
        self.new_name.setPlaceholderText("Nombre del tema (ej: Python, Tensores…)")
        row.addWidget(self.new_name)
        btn_add = QPushButton("+ Agregar")
        btn_add.setStyleSheet(btn_color(PALETTE['B1']))
        btn_add.clicked.connect(self._add_tema)
        row.addWidget(btn_add)
        lay.addLayout(row)

        btn_del = QPushButton("Eliminar seleccionado")
        btn_del.clicked.connect(self._del_tema)
        lay.addWidget(btn_del)

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        btns.rejected.connect(self.reject)
        lay.addWidget(btns)

    def _reload(self):
        self.list_w.clear()
        for t in self.data.get("b1_temas", []):
            item = QListWidgetItem(t["nombre"])
            item.setData(Qt.ItemDataRole.UserRole, t["id"])
            self.list_w.addItem(item)

    def _add_tema(self):
        name = self.new_name.text().strip()
        if not name: return
        new_id = str(datetime.now().timestamp())
        self.data.setdefault("b1_temas", []).append({"id": new_id, "nombre": name})
        save_data(self.data)
        self.new_name.clear()
        self._reload()

    def _del_tema(self):
        item = self.list_w.currentItem()
        if not item: return
        tid = item.data(Qt.ItemDataRole.UserRole)
        self.data["b1_temas"] = [t for t in self.data.get("b1_temas",[]) if t["id"]!=tid]
        save_data(self.data)
        self._reload()

# ─────────────────────────────────────────────────────────────────────────────
#  TAB: HORARIO
# ─────────────────────────────────────────────────────────────────────────────
class HorarioTab(QWidget):
    registro_added = pyqtSignal()

    def __init__(self, data):
        super().__init__()
        self.data = data
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16,16,16,16)
        lay.setSpacing(12)

        # Header
        header = QHBoxLayout()
        today = date.today()
        self.week_label = Label(f"Semana del {self._monday().strftime('%d %b')} al {self._sunday().strftime('%d %b %Y')}",
                                14, bold=True)
        header.addWidget(self.week_label)
        header.addStretch()

        tip = Label("Clic en una celda LIBRE para asignar bloque o registrar", 11, PALETTE['muted'], italic=True)
        header.addWidget(tip)
        lay.addLayout(header)

        # Legend
        leg_row = QHBoxLayout()
        leg_row.setSpacing(8)
        for key, (name, color) in {**SCHEDULE_TYPES, **{k:v for k,v in BLOQUES.items() if k not in SCHEDULE_TYPES}}.items():
            if key in ("B1","B2","B3","B4","EJ","LIBRE"):
                pill = Label(f"  {name}  ", 11, color)
                pill.setStyleSheet(f"background:{color}22; color:{color}; border:1px solid {color}44; border-radius:10px; padding:3px 10px;")
                leg_row.addWidget(pill)
        leg_row.addStretch()
        lay.addLayout(leg_row)

        # Table
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea{border:none;background:transparent;}")
        container = QWidget()
        self.grid = QGridLayout(container)
        self.grid.setSpacing(2)
        scroll.setWidget(container)
        lay.addWidget(scroll)

        self._build_table()

    def _monday(self):
        today = date.today()
        return today - timedelta(days=today.weekday())

    def _sunday(self):
        return self._monday() + timedelta(days=6)

    def _build_table(self):
        # Clear
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget(): item.widget().deleteLater()

        today_col = date.today().weekday()  # 0=Monday

        # Headers
        corner = Label("Hora", 11, PALETTE['muted'])
        corner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        corner.setStyleSheet(f"background:{PALETTE['surface2']}; border-radius:6px; padding:8px;")
        self.grid.addWidget(corner, 0, 0)

        monday = self._monday()
        for c, day in enumerate(DAYS_ES):
            d = monday + timedelta(days=c)
            is_today = (c == today_col)
            color = PALETTE['B1'] if is_today else PALETTE['muted']
            lbl = Label(f"{day}\n{d.strftime('%d')}", 11, color, bold=is_today)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            bg = PALETTE['surface3'] if is_today else PALETTE['surface2']
            lbl.setStyleSheet(f"background:{bg}; border-radius:6px; padding:6px;")
            self.grid.addWidget(lbl, 0, c+1)

        # Cells
        sched = self.data.get("schedule", {})
        for r, hour in enumerate(HOURS):
            time_lbl = Label(hour, 10, PALETTE['muted'])
            time_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            time_lbl.setStyleSheet(f"background:{PALETTE['surface2']}; border-radius:5px; padding:4px 8px; min-width:54px;")
            self.grid.addWidget(time_lbl, r+1, 0)

            for c in range(7):
                base_type, base_text = BASE_SCHEDULE.get(hour, {}).get(c, ("LIBRE",""))
                # Override from user schedule
                cell_key = f"{hour}_{c}"
                if cell_key in sched:
                    cell_type = sched[cell_key]["type"]
                    cell_text = sched[cell_key].get("text","")
                else:
                    cell_type, cell_text = base_type, base_text

                btn = self._make_cell(hour, c, cell_type, cell_text, today_col)
                self.grid.addWidget(btn, r+1, c+1)

        # Column stretches
        self.grid.setColumnStretch(0, 0)
        for c in range(7):
            self.grid.setColumnStretch(c+1, 1)

    def _make_cell(self, hour, day_col, cell_type, cell_text, today_col):
        info = SCHEDULE_TYPES.get(cell_type, ("?", PALETTE['muted']))
        color = info[1]
        is_today = (day_col == today_col)
        is_libre = cell_type in ("LIBRE","B1","B2","B3","B4")

        display = cell_text if cell_text else info[0]
        btn = QPushButton(display)
        btn.setFixedHeight(38)
        btn.setFont(QFont("Segoe UI", 10))

        if cell_type == "LIBRE":
            bg = PALETTE['surface2'] if not is_today else PALETTE['surface3']
            bdr = "#2a3555" if is_today else PALETTE['border']
            btn.setStyleSheet(f"""
                QPushButton {{
                    background:{bg}; color:{PALETTE['dim']};
                    border:1px dashed {bdr}; border-radius:6px;
                    font-size:11px;
                }}
                QPushButton:hover {{
                    background:{PALETTE['surface3']}; color:{PALETTE['muted']};
                    border-style:solid;
                }}
            """)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, h=hour, d=day_col: self._cell_click(h, d))
        elif cell_type in ("B1","B2","B3","B4"):
            btn.setStyleSheet(f"""
                QPushButton {{
                    background:{color}22; color:{color};
                    border:1px solid {color}55; border-radius:6px;
                    font-size:11px; font-weight:600;
                }}
                QPushButton:hover {{ background:{color}44; }}
            """)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.clicked.connect(lambda _, h=hour, d=day_col, bl=cell_type: self._register_block(h, d, bl))
        else:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background:{color}18; color:{color};
                    border:1px solid {color}33; border-radius:6px;
                    font-size:11px;
                }}
                QPushButton:hover {{ background:{color}30; }}
            """)
            if cell_type == "EJ":
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.clicked.connect(lambda _, h=hour, d=day_col: self._register_block(h, d, "EJ"))
        return btn

    def _cell_click(self, hour, day_col):
        """Click on a LIBRE cell — assign a block type."""
        dlg = AssignBlockDialog(self.data, hour, day_col, self)
        if dlg.exec():
            block_type = dlg.get_type()
            cell_key = f"{hour}_{day_col}"
            self.data.setdefault("schedule", {})[cell_key] = {"type": block_type, "text": BLOQUES.get(block_type,("",""))[0]}
            save_data(self.data)
            self._build_table()

    def _register_block(self, hour, day_col, bloque):
        dlg = RegistrarDialog(self.data, bloque, self)
        if dlg.exec():
            reg = dlg.get_registro()
            self.data.setdefault("registros", []).append(reg)
            save_data(self.data)
            self.registro_added.emit()

    def refresh(self):
        self._build_table()

class AssignBlockDialog(QDialog):
    def __init__(self, data, hour, day_col, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Asignar bloque")
        self.setStyleSheet(GLOBAL_STYLE)
        self.setFixedWidth(320)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(20,20,20,20)
        lay.setSpacing(12)
        bnames = data.get("b_nombres", {})
        lay.addWidget(Label(f"Asignar {DAYS_ES[day_col]} {hour}", 14, bold=True))
        lay.addWidget(Label("¿Qué bloque usarás en este espacio?", 12, PALETTE['muted']))
        self.cb = QComboBox()
        for k,(default_name,color) in BLOQUES.items():
            name = bnames.get(k, default_name) if k != "EJ" else "Ejercicio"
            self.cb.addItem(f"{k} — {name}", k)
        lay.addWidget(self.cb)
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        lay.addWidget(btns)

    def get_type(self):
        return self.cb.currentData()

# ─────────────────────────────────────────────────────────────────────────────
#  TAB: REGISTRO DIARIO
# ─────────────────────────────────────────────────────────────────────────────
class RegistroTab(QWidget):
    registro_added = pyqtSignal()

    def __init__(self, data):
        super().__init__()
        self.data = data
        self._build()

    def _build(self):
        lay = QHBoxLayout(self)
        lay.setContentsMargins(16,16,16,16)
        lay.setSpacing(16)

        # LEFT — quick register
        left = QWidget()
        left.setMaximumWidth(340)
        left_lay = QVBoxLayout(left)
        left_lay.setSpacing(14)

        left_lay.addWidget(Label("Registrar sesión", 16, bold=True))
        left_lay.addWidget(Label("Añade una sesión completada.", 12, PALETTE['muted']))
        left_lay.addWidget(Separator())

        # Block buttons
        left_lay.addWidget(Label("Inicio rápido:", 12, PALETTE['muted']))
        grid_btns = QGridLayout()
        grid_btns.setSpacing(8)
        bnames = self.data.get("b_nombres", {})
        for i,(k,(def_name,color)) in enumerate(BLOQUES.items()):
            name = bnames.get(k, def_name) if k!="EJ" else "Ejercicio"
            b = QPushButton(f"{k}\n{name}")
            b.setFixedHeight(64)
            b.setStyleSheet(btn_color(color))
            b.clicked.connect(lambda _, bl=k: self._quick_register(bl))
            grid_btns.addWidget(b, i//2, i%2)
        left_lay.addLayout(grid_btns)

        left_lay.addWidget(Separator())
        btn_temas = QPushButton("⚙ Administrar temas B1")
        btn_temas.clicked.connect(self._manage_temas)
        left_lay.addWidget(btn_temas)

        # Rename blocks
        left_lay.addWidget(Label("Renombrar bloques:", 12, PALETTE['muted']))
        self.rename_inputs = {}
        bnames = self.data.get("b_nombres", {})
        for k in ("B1","B2","B3","B4"):
            row = QHBoxLayout()
            row.addWidget(Label(f"{k}:", 12, BLOQUES[k][1], bold=True))
            inp = QLineEdit(bnames.get(k, BLOQUES[k][0]))
            self.rename_inputs[k] = inp
            row.addWidget(inp)
            left_lay.addLayout(row)
        btn_rename = QPushButton("Guardar nombres")
        btn_rename.clicked.connect(self._save_names)
        left_lay.addWidget(btn_rename)

        left_lay.addStretch()
        lay.addWidget(left)

        # RIGHT — history list
        right = QWidget()
        right_lay = QVBoxLayout(right)
        right_lay.setSpacing(10)

        header = QHBoxLayout()
        header.addWidget(Label("Historial de sesiones", 15, bold=True))
        header.addStretch()
        btn_del = QPushButton("Eliminar seleccionado")
        btn_del.clicked.connect(self._delete_selected)
        header.addWidget(btn_del)
        right_lay.addLayout(header)

        self.list_w = QListWidget()
        self.list_w.setAlternatingRowColors(False)
        right_lay.addWidget(self.list_w)

        lay.addWidget(right)
        self.refresh()

    def _quick_register(self, bloque):
        dlg = RegistrarDialog(self.data, bloque, self)
        if dlg.exec():
            reg = dlg.get_registro()
            self.data.setdefault("registros",[]).append(reg)
            save_data(self.data)
            self.refresh()
            self.registro_added.emit()

    def _manage_temas(self):
        dlg = TemasB1Dialog(self.data, self)
        dlg.exec()

    def _save_names(self):
        self.data.setdefault("b_nombres",{})
        for k, inp in self.rename_inputs.items():
            self.data["b_nombres"][k] = inp.text().strip() or BLOQUES[k][0]
        save_data(self.data)

    def _delete_selected(self):
        row = self.list_w.currentRow()
        if row < 0: return
        idx = self.list_w.currentItem().data(Qt.ItemDataRole.UserRole)
        if idx is not None and QMessageBox.question(self,"Eliminar","¿Eliminar este registro?") == QMessageBox.StandardButton.Yes:
            self.data["registros"].pop(idx)
            save_data(self.data)
            self.refresh()
            self.registro_added.emit()

    def refresh(self):
        self.list_w.clear()
        registros = self.data.get("registros",[])
        bnames = self.data.get("b_nombres",{})
        temas = {t["id"]:t["nombre"] for t in self.data.get("b1_temas",[])}
        for i, reg in enumerate(reversed(registros)):
            bl = reg["bloque"]
            color = BLOQUES.get(bl, ("?","#888"))[1]
            name  = bnames.get(bl, BLOQUES.get(bl,("?",""))[0]) if bl!="EJ" else "Ejercicio"
            subtema = ""
            if reg.get("subtema"):
                subtema = f" › {temas.get(reg['subtema'],'?')}"
            nota = f" — {reg['nota']}" if reg.get("nota") else ""
            text = f"  {reg['date']}  ·  {bl} {name}{subtema}  ·  {reg['horas']}h{nota}"
            item = QListWidgetItem(text)
            item.setForeground(QColor(color))
            item.setData(Qt.ItemDataRole.UserRole, len(registros)-1-i)
            self.list_w.addItem(item)

# ─────────────────────────────────────────────────────────────────────────────
#  TAB: ESTADÍSTICAS
# ─────────────────────────────────────────────────────────────────────────────
class EstadisticasTab(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self._build()
        self.refresh()

    def _build(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(16,16,16,16)
        outer.setSpacing(14)

        # Range selector
        top = QHBoxLayout()
        top.addWidget(Label("Período:", 13, PALETTE['muted']))
        self.range_cb = QComboBox()
        self.range_cb.addItems(["Última semana","Últimos 30 días","Últimos 90 días","Todo el tiempo"])
        self.range_cb.currentIndexChanged.connect(self.refresh)
        top.addWidget(self.range_cb)
        top.addStretch()
        outer.addLayout(top)

        # KPIs
        self.kpi_row = QHBoxLayout()
        self.kpi_row.setSpacing(10)
        outer.addLayout(self.kpi_row)

        # Scroll for charts
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea{border:none;}")
        container = QWidget()
        self.charts_lay = QVBoxLayout(container)
        self.charts_lay.setSpacing(16)
        scroll.setWidget(container)
        outer.addWidget(scroll)

    def _date_limit(self):
        idx = self.range_cb.currentIndex()
        if idx == 0: return date.today() - timedelta(days=7)
        if idx == 1: return date.today() - timedelta(days=30)
        if idx == 2: return date.today() - timedelta(days=90)
        return date(2000,1,1)

    def refresh(self):
        self._clear_kpis()
        self._clear_charts()

        registros = self.data.get("registros",[])
        temas     = {t["id"]:t["nombre"] for t in self.data.get("b1_temas",[])}
        bnames    = self.data.get("b_nombres",{})
        limit     = self._date_limit()

        filtered = []
        for r in registros:
            try:
                d = datetime.strptime(r["date"],"%Y-%m-%d").date()
                if d >= limit: filtered.append((d,r))
            except: pass

        # ── KPIs ──
        total = sum(r["horas"] for _,r in filtered)
        by_block = defaultdict(float)
        for _,r in filtered: by_block[r["bloque"]] += r["horas"]

        kpis = [
            ("Total horas", f"{total:.1f}h", PALETTE['text']),
            ("B1 Aprendizaje", f"{by_block['B1']:.1f}h", PALETTE['B1']),
            ("B2 Proyectos",   f"{by_block['B2']:.1f}h", PALETTE['B2']),
            ("B3 Habilidades", f"{by_block['B3']:.1f}h", PALETTE['B3']),
            ("Ejercicio",      f"{by_block['EJ']:.1f}h", PALETTE['EJ']),
            ("Sesiones",       str(len(filtered)), PALETTE['muted']),
        ]
        for label, val, color in kpis:
            card = KpiCard(label, val, color)
            card.setMinimumWidth(110)
            self.kpi_row.addWidget(card)

        if not filtered:
            self.charts_lay.addWidget(Label("Sin datos para el período seleccionado.", 13, PALETTE['muted'], italic=True))
            return

        # ── GRÁFICO 1: Horas acumuladas por bloque (barras) ──
        self._add_section_label("Horas por bloque")
        canvas1 = MplCanvas(8, 3.2)
        ax = canvas1.fig.add_subplot(111)
        ax.set_facecolor(PALETTE['surface'])
        canvas1.fig.patch.set_facecolor(PALETTE['surface'])
        blocks  = [b for b in BLOQUES if by_block[b]>0]
        colors  = [BLOQUES[b][1] for b in blocks]
        values  = [by_block[b] for b in blocks]
        labels  = [bnames.get(b,BLOQUES[b][0]) if b!="EJ" else "Ejercicio" for b in blocks]
        bars = ax.bar(labels, values, color=[c+"cc" for c in colors], width=0.5,
                      edgecolor=[c for c in colors], linewidth=1.2)
        for bar, v in zip(bars, values):
            ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.05, f"{v:.1f}h",
                    ha='center', va='bottom', color=PALETTE['text'], fontsize=10, fontweight='600')
        ax.set_ylabel("Horas", color=PALETTE['muted'], fontsize=10)
        ax.tick_params(colors=PALETTE['muted'])
        ax.spines[:].set_color(PALETTE['border'])
        ax.set_facecolor(PALETTE['surface'])
        for sp in ax.spines.values(): sp.set_color(PALETTE['border'])
        canvas1.fig.tight_layout()
        self.charts_lay.addWidget(canvas1)

        # ── GRÁFICO 2: Progreso diario acumulado ──
        self._add_section_label("Progreso acumulado en el tiempo")
        canvas2 = MplCanvas(8, 3.2)
        ax2 = canvas2.fig.add_subplot(111)
        ax2.set_facecolor(PALETTE['surface'])
        canvas2.fig.patch.set_facecolor(PALETTE['surface'])

        by_date = defaultdict(lambda: defaultdict(float))
        for d, r in sorted(filtered): by_date[d][r["bloque"]] += r["horas"]

        if by_date:
            all_dates = sorted(by_date.keys())
            import matplotlib.dates as mdates
            for bl, color in [(b,BLOQUES[b][1]) for b in BLOQUES]:
                daily = [by_date[d].get(bl,0) for d in all_dates]
                cumul = list(np.cumsum(daily))
                if any(v>0 for v in cumul):
                    name = bnames.get(bl,BLOQUES[bl][0]) if bl!="EJ" else "Ejercicio"
                    ax2.plot(all_dates, cumul, color=color, linewidth=2.5,
                             label=name, marker='o', markersize=4)
                    ax2.fill_between(all_dates, cumul, alpha=0.08, color=color)

            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
            ax2.legend(fontsize=9, facecolor=PALETTE['surface2'],
                       labelcolor=PALETTE['text'], edgecolor=PALETTE['border'])
        ax2.set_ylabel("Horas acumuladas", color=PALETTE['muted'], fontsize=10)
        ax2.tick_params(colors=PALETTE['muted'])
        for sp in ax2.spines.values(): sp.set_color(PALETTE['border'])
        canvas2.fig.tight_layout()
        self.charts_lay.addWidget(canvas2)

        # ── GRÁFICO 3: Donut distribución ──
        self._add_section_label("Distribución de tiempo")
        canvas3 = MplCanvas(6, 3.5)
        ax3 = canvas3.fig.add_subplot(111)
        canvas3.fig.patch.set_facecolor(PALETTE['surface'])
        ax3.set_facecolor(PALETTE['surface'])
        if any(by_block[b]>0 for b in BLOQUES):
            sizes  = [by_block[b] for b in BLOQUES if by_block[b]>0]
            clrs   = [BLOQUES[b][1] for b in BLOQUES if by_block[b]>0]
            lbls   = [bnames.get(b,BLOQUES[b][0]) if b!="EJ" else "Ejercicio" for b in BLOQUES if by_block[b]>0]
            wedges, texts, autotexts = ax3.pie(
                sizes, labels=lbls, colors=[c+"cc" for c in clrs],
                autopct='%1.1f%%', pctdistance=0.75,
                wedgeprops=dict(width=0.55, edgecolor=PALETTE['surface'], linewidth=2)
            )
            for t in texts: t.set_color(PALETTE['muted']); t.set_fontsize(9)
            for at in autotexts: at.set_color(PALETTE['text']); at.set_fontsize(9); at.set_fontweight('bold')
        canvas3.fig.tight_layout()
        self.charts_lay.addWidget(canvas3)

        # ── GRÁFICO 4: B1 por subtema ──
        b1_recs = [(d,r) for d,r in filtered if r["bloque"]=="B1" and r.get("subtema")]
        if b1_recs:
            self._add_section_label("B1 — Horas por subtema de aprendizaje")
            canvas4 = MplCanvas(8, 3.0)
            ax4 = canvas4.fig.add_subplot(111)
            ax4.set_facecolor(PALETTE['surface'])
            canvas4.fig.patch.set_facecolor(PALETTE['surface'])
            by_tema = defaultdict(float)
            for _,r in b1_recs: by_tema[temas.get(r["subtema"],"?")] += r["horas"]
            items = sorted(by_tema.items(), key=lambda x:-x[1])
            names = [i[0] for i in items]
            vals  = [i[1] for i in items]
            colors_b1 = [PALETTE['B1']+"cc"]*len(names)
            bars4 = ax4.barh(names, vals, color=colors_b1,
                             edgecolor=PALETTE['B1'], linewidth=1.0, height=0.5)
            for bar, v in zip(bars4, vals):
                ax4.text(v+0.05, bar.get_y()+bar.get_height()/2,
                         f"{v:.1f}h", va='center', color=PALETTE['text'], fontsize=10, fontweight='600')
            ax4.set_xlabel("Horas", color=PALETTE['muted'], fontsize=10)
            ax4.tick_params(colors=PALETTE['muted'])
            for sp in ax4.spines.values(): sp.set_color(PALETTE['border'])
            ax4.invert_yaxis()
            canvas4.fig.tight_layout()
            self.charts_lay.addWidget(canvas4)

        # ── GRÁFICO 5: Heatmap horas por día de semana ──
        self._add_section_label("Actividad por día de la semana")
        canvas5 = MplCanvas(8, 2.8)
        ax5 = canvas5.fig.add_subplot(111)
        ax5.set_facecolor(PALETTE['surface'])
        canvas5.fig.patch.set_facecolor(PALETTE['surface'])
        day_hrs = defaultdict(float)
        for d, r in filtered: day_hrs[d.weekday()] += r["horas"]
        days_order = list(range(7))
        hvals = [day_hrs[d] for d in days_order]
        bar_colors = [PALETTE['B1']+"cc" if v==max(hvals) else PALETTE['surface3'] for v in hvals]
        bars5 = ax5.bar([d[:3] for d in DAYS_ES], hvals, color=bar_colors,
                        edgecolor=[PALETTE['B1'] if v==max(hvals) else PALETTE['border'] for v in hvals],
                        linewidth=1.0, width=0.6)
        for bar, v in zip(bars5, hvals):
            if v > 0:
                ax5.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.05,
                         f"{v:.0f}h", ha='center', va='bottom',
                         color=PALETTE['text'], fontsize=9)
        ax5.set_ylabel("Horas", color=PALETTE['muted'], fontsize=10)
        ax5.tick_params(colors=PALETTE['muted'])
        for sp in ax5.spines.values(): sp.set_color(PALETTE['border'])
        canvas5.fig.tight_layout()
        self.charts_lay.addWidget(canvas5)

        # ── GRÁFICO 6: Racha semanal ──
        self._add_section_label("Horas por semana (últimas 12 semanas)")
        canvas6 = MplCanvas(8, 2.8)
        ax6 = canvas6.fig.add_subplot(111)
        ax6.set_facecolor(PALETTE['surface'])
        canvas6.fig.patch.set_facecolor(PALETTE['surface'])
        week_hrs = defaultdict(float)
        for d, r in filtered:
            week_start = d - timedelta(days=d.weekday())
            week_hrs[week_start] += r["horas"]
        if week_hrs:
            weeks = sorted(week_hrs.keys())[-12:]
            wvals = [week_hrs[w] for w in weeks]
            wlbls = [w.strftime("%d/%m") for w in weeks]
            wcolors = [PALETTE['EJ']+"cc" if v==max(wvals) else PALETTE['surface3'] for v in wvals]
            ax6.bar(wlbls, wvals, color=wcolors,
                    edgecolor=[PALETTE['EJ'] if v==max(wvals) else PALETTE['border'] for v in wvals],
                    linewidth=1.0, width=0.6)
            ax6.set_ylabel("Horas", color=PALETTE['muted'], fontsize=10)
            ax6.tick_params(axis='x', rotation=30, colors=PALETTE['muted'], labelsize=9)
            ax6.tick_params(axis='y', colors=PALETTE['muted'])
        for sp in ax6.spines.values(): sp.set_color(PALETTE['border'])
        canvas6.fig.tight_layout()
        self.charts_lay.addWidget(canvas6)

        self.charts_lay.addStretch()

    def _add_section_label(self, text):
        lbl = Label(text, 13, PALETTE['muted'], bold=True)
        lbl.setStyleSheet(f"color:{PALETTE['muted']}; font-size:12px; font-weight:600; "
                          f"border-bottom:1px solid {PALETTE['border']}; padding-bottom:4px; margin-top:8px;")
        self.charts_lay.addWidget(lbl)

    def _clear_kpis(self):
        while self.kpi_row.count():
            item = self.kpi_row.takeAt(0)
            if item.widget(): item.widget().deleteLater()

    def _clear_charts(self):
        while self.charts_lay.count():
            item = self.charts_lay.takeAt(0)
            if item.widget(): item.widget().deleteLater()

# ─────────────────────────────────────────────────────────────────────────────
#  VENTANA PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = load_data()
        self.setWindowTitle("Panel de Productividad")
        self.setMinimumSize(1100, 720)
        self.setStyleSheet(GLOBAL_STYLE)

        central = QWidget()
        self.setCentralWidget(central)
        main_lay = QVBoxLayout(central)
        main_lay.setContentsMargins(0,0,0,0)
        main_lay.setSpacing(0)

        # Top bar
        topbar = QWidget()
        topbar.setFixedHeight(52)
        topbar.setStyleSheet(f"background:{PALETTE['surface']}; border-bottom:1px solid {PALETTE['border']};")
        tbl = QHBoxLayout(topbar)
        tbl.setContentsMargins(20,0,20,0)
        logo = Label("Panel  ", 15, PALETTE['text'], bold=True)
        logo.setStyleSheet(f"font-family:'Segoe UI'; color:{PALETTE['text']}; font-size:15px; font-weight:700;")
        tbl.addWidget(logo)
        span = Label("Productividad", 15, PALETTE['B1'])
        span.setStyleSheet(f"color:{PALETTE['B1']}; font-size:15px; font-style:italic;")
        tbl.addWidget(span)
        tbl.addStretch()

        today_lbl = Label(date.today().strftime("%A, %d de %B de %Y"), 12, PALETTE['muted'])
        tbl.addWidget(today_lbl)
        main_lay.addWidget(topbar)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        self.horario_tab  = HorarioTab(self.data)
        self.registro_tab = RegistroTab(self.data)
        self.stats_tab    = EstadisticasTab(self.data)

        self.tabs.addTab(self.horario_tab,  "📅  Horario")
        self.tabs.addTab(self.registro_tab, "✏️  Registrar")
        self.tabs.addTab(self.stats_tab,    "📊  Estadísticas")

        # Connect signals
        self.horario_tab.registro_added.connect(self._on_new_registro)
        self.registro_tab.registro_added.connect(self._on_new_registro)
        self.tabs.currentChanged.connect(self._on_tab_change)

        main_lay.addWidget(self.tabs)

    def _on_new_registro(self):
        self.registro_tab.refresh()
        if self.tabs.currentIndex() == 2:
            self.stats_tab.refresh()

    def _on_tab_change(self, idx):
        if idx == 2:
            self.stats_tab.refresh()
        elif idx == 1:
            self.registro_tab.refresh()

# ─────────────────────────────────────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Panel de Productividad")
    app.setStyle("Fusion")

    # Dark palette for native widgets
    pal = QPalette()
    pal.setColor(QPalette.ColorRole.Window,          QColor(PALETTE['bg']))
    pal.setColor(QPalette.ColorRole.WindowText,      QColor(PALETTE['text']))
    pal.setColor(QPalette.ColorRole.Base,            QColor(PALETTE['surface']))
    pal.setColor(QPalette.ColorRole.AlternateBase,   QColor(PALETTE['surface2']))
    pal.setColor(QPalette.ColorRole.Text,            QColor(PALETTE['text']))
    pal.setColor(QPalette.ColorRole.Button,          QColor(PALETTE['surface2']))
    pal.setColor(QPalette.ColorRole.ButtonText,      QColor(PALETTE['text']))
    pal.setColor(QPalette.ColorRole.Highlight,       QColor(PALETTE['B1']))
    pal.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    app.setPalette(pal)

    w = MainWindow()
    w.show()
    sys.exit(app.exec())
