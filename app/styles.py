import os

# =========================
# 🎨 PALETTES
# =========================

PALETTE_DARK = {
    "bg": "#08090c",
    "surface": "#0f1117",
    "surface2": "#161820",
    "surface3": "#1c1f2a",
    "border": "#1e2133",
    "text": "#dde1ec",
    "muted": "#8a92ab",
    "dim": "#5a6075",
    "B1": "#a78bfa",
    "B2": "#38bdf8",
    "B3": "#2dd4bf",
    "B4": "#fb923c",
    "EJ": "#22c55e",
    "clase": "#818cf8",
}

PALETTE_LIGHT = {
    "bg": "#f5f7fb",
    "surface": "#ffffff",
    "surface2": "#eef2f7",
    "surface3": "#e2e8f0",
    "border": "#cbd5e1",
    "text": "#0f172a",
    "muted": "#64748b",
    "dim": "#94a3b8",
    "B1": "#7c3aed",
    "B2": "#0284c7",
    "B3": "#0f766e",
    "B4": "#ea580c",
    "EJ": "#16a34a",
    "clase": "#4f46e5",
}


def get_palette(mode=None):
    """Retorna paleta activa en función del modo (dark/light)."""
    selected = (mode or os.getenv("PRODUCTIVIDAD_THEME", "dark")).strip().lower()
    return PALETTE_LIGHT if selected == "light" else PALETTE_DARK


# =========================
# 🎛 STYLE GENERATOR
# =========================

def get_global_style(palette):
    return f"""
    QMainWindow, QWidget {{
        background: {palette['bg']};
        color: {palette['text']};
        font-family: 'Segoe UI', 'Ubuntu', sans-serif;
        font-size: 13px;
    }}

    QTabWidget::pane {{
        border: 1px solid {palette['border']};
        background: {palette['surface']};
        border-radius: 8px;
    }}

    QTabBar::tab {{
        background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
            stop:0 {palette['surface2']},
            stop:1 {palette['surface']}
        );
        color: {palette['muted']};
        padding: 10px 22px;
        border-radius: 6px;
        margin-right: 4px;
        font-weight: 600;
        border: 1px solid {palette['border']};
    }}

    QTabBar::tab:selected {{
        background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
            stop:0 {palette['surface3']},
            stop:1 {palette['surface2']}
        );
        color: {palette['text']};
        border: 1px solid {palette['B1']}66;
    }}

    QTabBar::tab:hover {{
        color: {palette['text']};
        background: {palette['surface2']};
    }}

    QPushButton {{
        background: qlineargradient(x1:0,y1:0,x2:0,y2:1,
            stop:0 {palette['surface2']},
            stop:1 {palette['surface']}
        );
        color: {palette['text']};
        border: 1px solid {palette['border']};
        border-radius: 8px;
        padding: 8px 18px;
        font-weight: 600;
    }}

    QPushButton:hover {{
        background: {palette['surface3']};
        border-color: {palette['B1']};
    }}

    QPushButton:pressed {{
        background: {palette['dim']};
        border-color: {palette['B1']}77;
    }}

    QPushButton:disabled {{
        color: {palette['muted']};
        border-color: {palette['border']};
    }}

    QLineEdit, QTextEdit, QDoubleSpinBox, QSpinBox, QComboBox {{
        background: {palette['surface2']};
        color: {palette['text']};
        border: 1px solid {palette['border']};
        border-radius: 7px;
        padding: 7px 11px;
        selection-background-color: {palette['B1']};
    }}

    QLineEdit:focus, QTextEdit:focus, QDoubleSpinBox:focus,
    QSpinBox:focus, QComboBox:focus {{
        border: 1px solid {palette['B1']};
        background: {palette['surface']};
    }}

    QComboBox::drop-down {{
        border: none;
        width: 20px;
    }}

    QComboBox QAbstractItemView {{
        background: {palette['surface2']};
        color: {palette['text']};
        border: 1px solid {palette['border']};
        selection-background-color: {palette['surface3']};
    }}

    QListWidget {{
        background: {palette['surface']};
        color: {palette['text']};
        border: 1px solid {palette['border']};
        border-radius: 8px;
        padding: 4px;
    }}

    QListWidget::item {{
        padding: 7px 10px;
        border-radius: 5px;
    }}

    QListWidget::item:selected {{
        background: {palette['surface3']};
    }}

    QListWidget::item:hover {{
        background: {palette['surface2']};
    }}

    QScrollBar:vertical {{
        background: {palette['bg']};
        width: 6px;
    }}

    QScrollBar::handle:vertical {{
        background: {palette['border']};
        border-radius: 3px;
    }}

    QScrollBar::add-line:vertical,
    QScrollBar::sub-line:vertical {{
        height: 0px;
    }}

    QGroupBox {{
        border: 1px solid {palette['border']};
        border-radius: 10px;
        margin-top: 14px;
        padding: 12px;
        color: {palette['muted']};
        font-size: 12px;
    }}

    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 12px;
        padding: 0 6px;
    }}

    QSplitter::handle {{
        background: {palette['border']};
    }}
    """


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


PALETTE = get_palette()
GLOBAL_STYLE = get_global_style(PALETTE)
