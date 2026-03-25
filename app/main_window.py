from datetime import date

from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QTabWidget, QVBoxLayout, QWidget

from .constants import PALETTE
from .data import load_data
from .styles import GLOBAL_STYLE
from .tabs import EstadisticasTab, HorarioTab, RegistroTab
from .widgets import Label


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
        main_lay.setContentsMargins(0, 0, 0, 0)
        main_lay.setSpacing(0)

        topbar = QWidget()
        topbar.setFixedHeight(52)
        topbar.setStyleSheet(f"background:{PALETTE['surface']}; border-bottom:1px solid {PALETTE['border']};")
        tbl = QHBoxLayout(topbar)
        tbl.setContentsMargins(20, 0, 20, 0)
        logo = Label("Panel  ", 15, PALETTE['text'], bold=True)
        logo.setStyleSheet(f"font-family:'Segoe UI'; color:{PALETTE['text']}; font-size:15px; font-weight:700;")
        tbl.addWidget(logo)
        span = Label("Productividad", 15, PALETTE['B1'])
        span.setStyleSheet(f"color:{PALETTE['B1']}; font-size:15px; font-style:italic;")
        tbl.addWidget(span)
        tbl.addStretch()
        tbl.addWidget(Label(date.today().strftime("%A, %d de %B de %Y"), 12, PALETTE['muted']))
        main_lay.addWidget(topbar)

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        self.horario_tab = HorarioTab(self.data)
        self.registro_tab = RegistroTab(self.data)
        self.stats_tab = EstadisticasTab(self.data)

        self.tabs.addTab(self.horario_tab, "📅  Horario")
        self.tabs.addTab(self.registro_tab, "✏️  Registrar")
        self.tabs.addTab(self.stats_tab, "📊  Estadísticas")

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
