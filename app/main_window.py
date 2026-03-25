from datetime import date
import os

from PyQt6.QtWidgets import QApplication, QFileDialog, QHBoxLayout, QMainWindow, QMessageBox, QPushButton, QTabWidget, QVBoxLayout, QWidget

from .constants import PALETTE
from .data import DATA_FILE, export_data, import_data, load_data, save_data
from .dialogs import SettingsDialog
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
        btn_import = QPushButton("Importar BD")
        btn_import.clicked.connect(self._import_db)
        tbl.addWidget(btn_import)
        btn_export = QPushButton("Exportar BD")
        btn_export.clicked.connect(self._export_db)
        tbl.addWidget(btn_export)
        btn_settings = QPushButton("⚙ Ajustes")
        btn_settings.clicked.connect(self._open_settings)
        tbl.addWidget(btn_settings)
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

    def _export_db(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar base de datos",
            DATA_FILE.replace(".json", "_export.json"),
            "JSON (*.json)",
        )
        if not path:
            return
        export_data(self.data, path)
        QMessageBox.information(self, "Exportación completada", f"Datos exportados en:\n{path}")

    def _import_db(self):
        path, _ = QFileDialog.getOpenFileName(self, "Importar base de datos", "", "JSON (*.json)")
        if not path:
            return
        try:
            self.data = import_data(path)
            save_data(self.data)
            self.horario_tab.data = self.data
            self.registro_tab.data = self.data
            self.stats_tab.data = self.data
            self.horario_tab.refresh()
            self.registro_tab.refresh()
            self.stats_tab.refresh()
            QMessageBox.information(self, "Importación completada", "La base de datos fue importada correctamente.")
        except Exception as exc:
            QMessageBox.critical(self, "Error al importar", f"No se pudo importar el archivo:\n{exc}")

    def _open_settings(self):
        dlg = SettingsDialog(self.data, self)
        if dlg.exec():
            self.data["settings"] = dlg.get_settings()
            save_data(self.data)
            app = QApplication.instance()
            if app:
                app.setStyleSheet(f"* {{ font-size: {self.data['settings']['font_size']}px; }}")
            os.environ["PRODUCTIVIDAD_THEME"] = self.data["settings"]["theme"]
            QMessageBox.information(
                self,
                "Ajustes guardados",
                "La fuente se aplicó de inmediato.\nPara aplicar completamente el tema, reinicia la aplicación.",
            )
