from .constants import PALETTE

GLOBAL_STYLE = f"""
QMainWindow, QWidget {{
    background: {PALETTE['bg']};
    color: {PALETTE['text']};
    font-family: 'Segoe UI', 'Ubuntu', sans-serif;
    font-size: 13px;
}}
QTabWidget::pane {{ border: 1px solid {PALETTE['border']}; background: {PALETTE['surface']}; border-radius: 8px; }}
QTabBar::tab {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {PALETTE['surface2']}, stop:1 {PALETTE['surface']});
    color: {PALETTE['muted']};
    padding: 10px 22px; border-radius: 6px; margin-right: 4px;
    font-weight: 600; font-size: 13px;
    border: 1px solid {PALETTE['border']};
}}
QTabBar::tab:selected {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {PALETTE['surface3']}, stop:1 {PALETTE['surface2']});
    color: {PALETTE['text']};
    border: 1px solid {PALETTE['B1']}66;
}}
QTabBar::tab:hover {{ color: {PALETTE['text']}; }}
QPushButton {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {PALETTE['surface2']}, stop:1 {PALETTE['surface']});
    color: {PALETTE['text']};
    border: 1px solid {PALETTE['border']}; border-radius: 8px;
    padding: 8px 18px; font-size: 13px; font-weight: 600;
}}
QPushButton:hover {{ background: {PALETTE['surface3']}; border-color: #3a4270; }}
QPushButton:pressed {{ background: {PALETTE['dim']}; border-color: {PALETTE['B1']}77; }}
QPushButton:disabled {{ color: {PALETTE['muted']}; border-color: {PALETTE['border']}; }}
QLineEdit, QTextEdit, QDoubleSpinBox, QSpinBox, QComboBox {{
    background: {PALETTE['surface2']}; color: {PALETTE['text']};
    border: 1px solid {PALETTE['border']}; border-radius: 7px;
    padding: 7px 11px; font-size: 13px;
    selection-background-color: {PALETTE['B1']};
}}
QLineEdit:focus, QTextEdit:focus, QDoubleSpinBox:focus, QSpinBox:focus, QComboBox:focus {{
    border: 1px solid {PALETTE['B1']}aa;
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
QScrollBar::handle:vertical {{
    background: qlineargradient(x1:0,y1:0,x2:0,y2:1, stop:0 {PALETTE['border']}, stop:1 {PALETTE['surface3']});
    border-radius: 3px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}
QGroupBox {{
    border: 1px solid {PALETTE['border']}; border-radius: 10px;
    margin-top: 14px; padding: 12px; color: {PALETTE['muted']}; font-size: 12px;
}}
QGroupBox::title {{ subcontrol-origin: margin; left: 12px; padding: 0 6px; }}
QSplitter::handle {{ background: {PALETTE['border']}; }}
"""


def btn_color(color):
    return f"""
        QPushButton {{
            background: {color}22; color: {color};
            border: 1px solid {color}55; border-radius: 8px;
            padding: 8px 16px; font-weight: 600;
        }}
        QPushButton:hover {{ background: {color}44; }}
        QPushButton:pressed {{ background: {color}66; }}
    """
