from datetime import date, datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QDoubleSpinBox,
)

from .constants import BLOQUES, DAYS_ES, PALETTE
from .data import save_data
from .styles import GLOBAL_STYLE, btn_color
from .widgets import Label, Separator


class RegistrarDialog(QDialog):
    def __init__(self, data, bloque_default=None, parent=None):
        super().__init__(parent)
        self.data = data
        self.setWindowTitle("Registrar sesión")
        self.setMinimumWidth(420)
        self.setStyleSheet(GLOBAL_STYLE + f"QDialog {{ background:{PALETTE['surface2']}; border-radius:14px; }}")

        lay = QVBoxLayout(self)
        lay.setSpacing(14)
        lay.setContentsMargins(24, 24, 24, 24)

        lay.addWidget(Label("Registrar sesión", 17, bold=True))
        lay.addWidget(Separator())

        row_f = QHBoxLayout()
        row_f.addWidget(Label("Fecha:", 13, PALETTE['muted']))
        self.fecha_edit = QLineEdit(str(date.today()))
        self.fecha_edit.setPlaceholderText("YYYY-MM-DD")
        row_f.addWidget(self.fecha_edit)
        lay.addLayout(row_f)

        row_b = QHBoxLayout()
        row_b.addWidget(Label("Bloque:", 13, PALETTE['muted']))
        self.bloque_cb = QComboBox()
        bnames = data.get("b_nombres", {})
        for k, (default_name, _) in BLOQUES.items():
            name = bnames.get(k, default_name) if k != "EJ" else "Ejercicio"
            self.bloque_cb.addItem(f"{k} — {name}", k)
        if bloque_default:
            idx = [self.bloque_cb.itemData(i) for i in range(self.bloque_cb.count())].index(bloque_default)
            self.bloque_cb.setCurrentIndex(idx)
        row_b.addWidget(self.bloque_cb)
        lay.addLayout(row_b)
        self.bloque_cb.currentIndexChanged.connect(self._on_bloque_change)

        row_h = QHBoxLayout()
        row_h.addWidget(Label("Horas:", 13, PALETTE['muted']))
        self.horas_spin = QDoubleSpinBox()
        self.horas_spin.setRange(0.25, 12.0)
        self.horas_spin.setSingleStep(0.25)
        self.horas_spin.setValue(1.0)
        self.horas_spin.setSuffix(" h")
        row_h.addWidget(self.horas_spin)
        lay.addLayout(row_h)

        self.b1_frame = QGroupBox("Subtema de aprendizaje (B1)")
        b1_lay = QVBoxLayout(self.b1_frame)
        self.tema_cb = QComboBox()
        self._reload_temas()
        b1_lay.addWidget(self.tema_cb)
        lay.addWidget(self.b1_frame)

        self.nota_edit = QLineEdit()
        self.nota_edit.setPlaceholderText("Nota opcional (¿qué trabajaste?)")
        lay.addWidget(self.nota_edit)

        self.tags_edit = QLineEdit()
        all_tags = ", ".join(self.data.get("tags", []))
        self.tags_edit.setPlaceholderText("Tags (separados por coma). Ej: Programación, Álgebra lineal")
        if all_tags:
            self.tags_edit.setToolTip(f"Etiquetas existentes: {all_tags}")
        lay.addWidget(self.tags_edit)

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
        raw_tags = [tag.strip() for tag in self.tags_edit.text().split(",")]
        tags = [tag for tag in raw_tags if tag]
        return {
            "date": self.fecha_edit.text().strip(),
            "bloque": self.bloque_cb.currentData(),
            "horas": self.horas_spin.value(),
            "subtema": self.tema_cb.currentData() if self.bloque_cb.currentData() == "B1" else None,
            "nota": self.nota_edit.text().strip(),
            "tags": tags,
        }


class TemasB1Dialog(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.setWindowTitle("Administrar temas B1")
        self.setMinimumSize(400, 420)
        self.setStyleSheet(GLOBAL_STYLE)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 20, 20, 20)
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
        if not name:
            return
        new_id = str(datetime.now().timestamp())
        self.data.setdefault("b1_temas", []).append({"id": new_id, "nombre": name})
        save_data(self.data)
        self.new_name.clear()
        self._reload()

    def _del_tema(self):
        item = self.list_w.currentItem()
        if not item:
            return
        tid = item.data(Qt.ItemDataRole.UserRole)
        self.data["b1_temas"] = [t for t in self.data.get("b1_temas", []) if t["id"] != tid]
        save_data(self.data)
        self._reload()


class AssignBlockDialog(QDialog):
    def __init__(self, data, hour, day_col, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Asignar bloque")
        self.setStyleSheet(GLOBAL_STYLE)
        self.setFixedWidth(320)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(12)
        bnames = data.get("b_nombres", {})
        lay.addWidget(Label(f"Asignar {DAYS_ES[day_col]} {hour}", 14, bold=True))
        lay.addWidget(Label("¿Qué bloque usarás en este espacio? (o limpiar)", 12, PALETTE['muted']))
        self.cb = QComboBox()
        self.cb.addItem("🧠 B* (sin asignar)", "LIBRE")
        for k, (default_name, _) in BLOQUES.items():
            name = bnames.get(k, default_name) if k != "EJ" else "Ejercicio"
            self.cb.addItem(f"{k} — {name}", k)
        lay.addWidget(self.cb)
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        lay.addWidget(btns)

    def get_type(self):
        return self.cb.currentData()


class TagsDialog(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.setWindowTitle("Administrar etiquetas")
        self.setMinimumSize(400, 420)
        self.setStyleSheet(GLOBAL_STYLE)

        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(12)
        lay.addWidget(Label("Etiquetas personalizadas", 16, bold=True))
        lay.addWidget(Label("Crea etiquetas como Programación, Álgebra lineal, FreeCAD…", 12, PALETTE["muted"]))
        lay.addWidget(Separator())

        self.list_w = QListWidget()
        self._reload()
        lay.addWidget(self.list_w)

        row = QHBoxLayout()
        self.new_name = QLineEdit()
        self.new_name.setPlaceholderText("Nombre de etiqueta")
        row.addWidget(self.new_name)
        btn_add = QPushButton("+ Agregar")
        btn_add.clicked.connect(self._add_tag)
        row.addWidget(btn_add)
        lay.addLayout(row)

        btn_del = QPushButton("Eliminar seleccionada")
        btn_del.clicked.connect(self._del_tag)
        lay.addWidget(btn_del)

        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        btns.rejected.connect(self.reject)
        lay.addWidget(btns)

    def _reload(self):
        self.list_w.clear()
        for tag in self.data.get("tags", []):
            self.list_w.addItem(QListWidgetItem(tag))

    def _add_tag(self):
        name = self.new_name.text().strip()
        if not name:
            return
        tags = self.data.setdefault("tags", [])
        if name not in tags:
            tags.append(name)
            tags.sort(key=str.lower)
            save_data(self.data)
        self.new_name.clear()
        self._reload()

    def _del_tag(self):
        item = self.list_w.currentItem()
        if not item:
            return
        name = item.text()
        self.data["tags"] = [t for t in self.data.get("tags", []) if t != name]
        save_data(self.data)
        self._reload()


class SettingsDialog(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.setWindowTitle("Configuración")
        self.setMinimumWidth(380)
        self.setStyleSheet(GLOBAL_STYLE)

        settings = self.data.setdefault("settings", {})
        lay = QVBoxLayout(self)
        lay.setContentsMargins(20, 20, 20, 20)
        lay.setSpacing(12)
        lay.addWidget(Label("Ajustes visuales y comportamiento", 16, bold=True))
        lay.addWidget(Separator())

        row_theme = QHBoxLayout()
        row_theme.addWidget(Label("Tema:", 12, PALETTE["muted"]))
        self.theme_cb = QComboBox()
        self.theme_cb.addItem("Dark (Obsidian Nord)", "dark")
        self.theme_cb.addItem("Light (Blue Topaz)", "light")
        current_theme = settings.get("theme", "dark")
        self.theme_cb.setCurrentIndex(0 if current_theme == "dark" else 1)
        row_theme.addWidget(self.theme_cb)
        lay.addLayout(row_theme)

        row_font = QHBoxLayout()
        row_font.addWidget(Label("Tamaño de fuente:", 12, PALETTE["muted"]))
        self.font_spin = QSpinBox()
        self.font_spin.setRange(11, 18)
        self.font_spin.setValue(int(settings.get("font_size", 13)))
        row_font.addWidget(self.font_spin)
        lay.addLayout(row_font)

        self.auto_cb = QCheckBox("Registro automático desde horario (solo día actual)")
        self.auto_cb.setChecked(bool(settings.get("auto_registro_horario", True)))
        lay.addWidget(self.auto_cb)

        lay.addWidget(Label("Nota: el cambio de tema se aplica al reiniciar la app.", 11, PALETTE["muted"], italic=True))
        btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)
        lay.addWidget(btns)

    def get_settings(self):
        return {
            "theme": self.theme_cb.currentData(),
            "font_size": self.font_spin.value(),
            "auto_registro_horario": self.auto_cb.isChecked(),
        }
