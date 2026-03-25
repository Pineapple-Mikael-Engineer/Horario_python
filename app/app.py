import sys

import matplotlib
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QApplication

from .constants import PALETTE
from .main_window import MainWindow

matplotlib.use("QtAgg")


def run_app():
    app = QApplication(sys.argv)
    app.setApplicationName("Panel de Productividad")
    app.setStyle("Fusion")

    pal = QPalette()
    pal.setColor(QPalette.ColorRole.Window, QColor(PALETTE['bg']))
    pal.setColor(QPalette.ColorRole.WindowText, QColor(PALETTE['text']))
    pal.setColor(QPalette.ColorRole.Base, QColor(PALETTE['surface']))
    pal.setColor(QPalette.ColorRole.AlternateBase, QColor(PALETTE['surface2']))
    pal.setColor(QPalette.ColorRole.Text, QColor(PALETTE['text']))
    pal.setColor(QPalette.ColorRole.Button, QColor(PALETTE['surface2']))
    pal.setColor(QPalette.ColorRole.ButtonText, QColor(PALETTE['text']))
    pal.setColor(QPalette.ColorRole.Highlight, QColor(PALETTE['B1']))
    pal.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    app.setPalette(pal)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
