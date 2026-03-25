from PyQt6.QtWidgets import QFrame, QLabel, QSizePolicy, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from .constants import PALETTE


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
        if italic:
            style += "font-style:italic;"
        self.setStyleSheet(style)
        self.setWordWrap(True)


class KpiCard(QFrame):
    def __init__(self, label, value, color, sub=""):
        super().__init__()
        self.setStyleSheet(
            f"""
            QFrame {{
                background: {PALETTE['surface']};
                border: 1px solid {color}33;
                border-left: 3px solid {color};
                border-radius: 10px; padding: 2px;
            }}
        """
        )
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 14, 16, 14)
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
