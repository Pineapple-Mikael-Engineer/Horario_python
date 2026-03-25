# =========================
# 🎨 PALETTES
# =========================

PALETTE_DARK = {
    "bg": "#2E3440",
    "surface": "#3B4252",
    "surface2": "#434C5E",
    "surface3": "#4C566A",

    "text": "#ECEFF4",
    "muted": "#D8DEE9",

    "border": "#4C566A",
    "dim": "#3B4252",

    "B1": "#88C0D0",
    "B2": "#81A1C1",
    "B3": "#5E81AC",

    "success": "#A3BE8C",
    "warning": "#EBCB8B",
    "danger": "#BF616A",
}

PALETTE_LIGHT = {
    "bg": "#F5F7FA",
    "surface": "#FFFFFF",
    "surface2": "#EEF2F7",
    "surface3": "#E2E8F0",

    "text": "#1E293B",
    "muted": "#64748B",

    "border": "#CBD5E1",
    "dim": "#E2E8F0",

    "B1": "#3B82F6",
    "B2": "#60A5FA",
    "B3": "#2563EB",

    "success": "#22C55E",
    "warning": "#F59E0B",
    "danger": "#EF4444",
}


# =========================
# 🎛 STYLE GENERATOR
# =========================

def get_global_style(PALETTE):
    return f"""
    QMainWindow, QWidget {{
        background: {PALETTE['bg']};
        color: {PALETTE['text']};
        font-family: 'Segoe UI', 'Ubuntu', sans-serif;
        font-size: 13px;
    }}

    QTabWidget::pane {{
        border: 1px solid {PALETTE['border']};
        background: {PALETTE['surface']};
        border-radius: 8px;
    }}

    QTabBar::tab {{
        background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
            stop:0 {PALETTE['surface2']},
            stop:1 {PALETTE['surface']}
        );
        color: {PALETTE['muted']};
        padding: 10px 22px;
        border-radius: 6px;
        margin-right: 4px;
        font-weight: 600;
        border: 1px solid {PALETTE['border']};
    }}

    QTabBar::tab:selected {{
        background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
            stop:0 {PALETTE['surface3']},
            stop:1 {PALETTE['surface2']}
        );
        color: {PALETTE['text']};
        border: 1px solid {PALETTE['B1']}66;
    }}

    QTabBar::tab:hover {{
        color: {PALETTE['text']};
        background: {PALETTE['surface2']};
    }}

    QPushButton {{
        background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
            stop:0 {PALETTE['surface2']},
            stop:1 {PALETTE['surface']}
        );
        color: {PALETTE['text']};
        border: 1px solid {PALETTE['border']};
        border-radius: 8px;
        padding: 8px 18px;
        font-weight: 600;
    }}

    QPushButton:hover {{
        background: {PALETTE['surface3']};
        border-color: {PALETTE['B1']};
    }}

    QPushButton:pressed {{
        background: {PALETTE['dim']};
        border-color: {PALETTE['B1']}77;
    }}

    QPushButton:disabled {{
        color: {PALETTE['muted']};
        border-color: {PALETTE['border']};
    }}

    QLineEdit, QTextEdit, QDoubleSpinBox, QSpinBox, QComboBox {{
        background: {PALETTE['surface2']};
        color: {PALETTE['text']};
        border: 1px solid {PALETTE['border']};
        border-radius: 7px;
        padding: 7px 11px;
        selection-background-color: {PALETTE['B1']};
    }}

    QLineEdit:focus, QTextEdit:focus, QDoubleSpinBox:focus,
    QSpinBox:focus, QComboBox:focus {{
        border: 1px solid {PALETTE['B1']};
        background: {PALETTE['surface']};
    }}

    QComboBox::drop-down {{
        border: none;
        width: 20px;
    }}

    QComboBox QAbstractItemView {{
        background: {PALETTE['surface2']};
        color: {PALETTE['text']};
        border: 1px solid {PALETTE['border']};
        selection-background-color: {PALETTE['surface3']};
    }}

    QListWidget {{
        background: {PALETTE['surface']};
        color: {PALETTE['text']};
        border: 1px solid {PALETTE['border']};
        border-radius: 8px;
        padding: 4px;
    }}

    QListWidget::item {{
        padding: 7px 10px;
        border-radius: 5px;
    }}

    QListWidget::item:selected {{
        background: {PALETTE['surface3']};
    }}

    QListWidget::item:hover {{
        background: {PALETTE['surface2']};
    }}

    QScrollBar:vertical {{
        background: {PALETTE['bg']};
        width: 6px;
    }}

    QScrollBar::handle:vertical {{
        background: {PALETTE['border']};
        border-radius: 3px;
    }}

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QGroupBox {{
        border: 1px solid {PALETTE['border']};
        border-radius: 10px;
        margin-top: 14px;
        padding: 12px;
        color: {PALETTE['muted']};
        font-size: 12px;
    }}

    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 12px;
        padding: 0 6px;
    }}

    QSplitter::handle {{
        background: {PALETTE['border']};
    }}
    """


# =========================
# 🎯 BUTTON COLOR HELPER
# =========================

def btn_color(color):
    return f"""
    QPushButton {{
        background: {color}22;
        color: {color};
        border: 1px solid {color}55;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
    }}

    QPushButton:hover {{
        background: {color}44;
    }}

    QPushButton:pressed {{
        background: {color}66;
    }}
    """


# =========================
# 🚀 USO
# =========================

if __name__= "__main__":

    # Cambia aquí el tema:
    PALETTE = PALETTE_DARK
    # PALETTE = PALETTE_LIGHT

    GLOBAL_STYLE = get_global_style(PALETTE)