from collections import defaultdict
from datetime import date, datetime, timedelta

import numpy as np
from matplotlib import dates as mdates
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from .constants import BASE_SCHEDULE, BLOQUES, DAYS_ES, HOURS, PALETTE, SCHEDULE_TYPES
from .data import save_data
from .dialogs import AssignBlockDialog, RegistrarDialog, TagsDialog, TemasB1Dialog
from .styles import btn_color
from .widgets import KpiCard, Label, MplCanvas, Separator


class HorarioTab(QWidget):
    registro_added = pyqtSignal()

    def __init__(self, data):
        super().__init__()
        self.data = data
        self._build()

    def _build(self):
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(12)

        header = QHBoxLayout()
        self.week_label = Label(f"Semana del {self._monday().strftime('%d %b')} al {self._sunday().strftime('%d %b %Y')}", 14, bold=True)
        header.addWidget(self.week_label)
        header.addStretch()
        tip = Label("Clic en una celda LIBRE para asignar bloque o registrar", 11, PALETTE['muted'], italic=True)
        header.addWidget(tip)
        lay.addLayout(header)

        leg_row = QHBoxLayout()
        leg_row.setSpacing(8)
        for key, (name, color) in {**SCHEDULE_TYPES, **{k: v for k, v in BLOQUES.items() if k not in SCHEDULE_TYPES}}.items():
            if key in ("B1", "B2", "B3", "B4", "EJ", "LIBRE"):
                pill = Label(f"  {name}  ", 11, color)
                pill.setStyleSheet(f"background:{color}22; color:{color}; border:1px solid {color}44; border-radius:10px; padding:3px 10px;")
                leg_row.addWidget(pill)
        leg_row.addStretch()
        lay.addLayout(leg_row)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea{border:none;background:transparent;}")
        container = QWidget()
        self.grid = QGridLayout(container)
        self.grid.setHorizontalSpacing(8)
        self.grid.setVerticalSpacing(8)
        self.grid.setContentsMargins(8, 8, 8, 8)
        scroll.setWidget(container)
        lay.addWidget(scroll)

        self._build_table()

    def _monday(self):
        return date.today() - timedelta(days=date.today().weekday())

    def _sunday(self):
        return self._monday() + timedelta(days=6)

    def _build_table(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        today_col = date.today().weekday()
        corner = Label("Hora", 13, PALETTE['muted'], bold=True)
        corner.setAlignment(Qt.AlignmentFlag.AlignCenter)
        corner.setStyleSheet(f"background:{PALETTE['surface2']}; border-radius:10px; padding:10px;")
        self.grid.addWidget(corner, 0, 0)

        monday = self._monday()
        for c, day in enumerate(DAYS_ES):
            d = monday + timedelta(days=c)
            is_today = c == today_col
            color = PALETTE['B1'] if is_today else PALETTE['muted']
            lbl = Label(f"{day}\n{d.strftime('%d')}", 12, color, bold=is_today)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            bg = PALETTE['surface3'] if is_today else PALETTE['surface2']
            lbl.setStyleSheet(f"background:{bg}; border-radius:10px; padding:8px 10px; min-height:58px;")
            self.grid.addWidget(lbl, 0, c + 1)

        sched = self.data.get("schedule", {})
        for r, hour in enumerate(HOURS):
            time_lbl = Label(hour, 11, PALETTE['muted'], bold=True)
            time_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            time_lbl.setStyleSheet(f"background:{PALETTE['surface2']}; border-radius:8px; padding:8px 10px; min-width:76px;")
            self.grid.addWidget(time_lbl, r + 1, 0)

            for c in range(7):
                base_type, base_text = BASE_SCHEDULE.get(hour, {}).get(c, ("LIBRE", ""))
                cell_key = f"{hour}_{c}"
                if cell_key in sched:
                    cell_type = sched[cell_key]["type"]
                    cell_text = sched[cell_key].get("text", "")
                else:
                    cell_type, cell_text = base_type, base_text
                editable = base_type == "LIBRE" and c == today_col
                self.grid.addWidget(self._make_cell(hour, c, cell_type, cell_text, today_col, editable), r + 1, c + 1)

        self.grid.setColumnMinimumWidth(0, 86)
        self.grid.setColumnStretch(0, 0)
        for c in range(7):
            self.grid.setColumnMinimumWidth(c + 1, 124)
            self.grid.setColumnStretch(c + 1, 1)

    def _make_cell(self, hour, day_col, cell_type, cell_text, today_col, editable=False):
        info = SCHEDULE_TYPES.get(cell_type, ("?", PALETTE['muted']))
        color = info[1]
        is_today = day_col == today_col

        display = cell_text if cell_text else info[0]
        btn = QPushButton(display)
        btn.setFixedHeight(44)
        btn.setFont(QFont("Segoe UI", 11))

        if cell_type == "LIBRE":
            bg = PALETTE['surface2'] if not is_today else PALETTE['surface3']
            bdr = color if is_today else PALETTE['border']
            btn.setStyleSheet(
                f"""
                QPushButton {{
                    background:{bg}; color:{PALETTE['text']};
                    border:1px dashed {bdr}; border-radius:6px;
                    font-size:12px; font-weight:600;
                }}
                QPushButton:hover {{
                    background:{PALETTE['surface3']}; color:{PALETTE['text']};
                    border-style:solid;
                }}
            """
            )
            if editable:
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.clicked.connect(lambda _, h=hour, d=day_col: self._cell_click(h, d))
        elif cell_type in ("B1", "B2", "B3", "B4"):
            btn.setStyleSheet(
                f"""
                QPushButton {{
                    background:{color}22; color:{color};
                    border:1px solid {color}55; border-radius:6px;
                    font-size:11px; font-weight:600;
                }}
                QPushButton:hover {{ background:{color}44; }}
            """
            )
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            if editable:
                btn.clicked.connect(lambda _, h=hour, d=day_col: self._cell_click(h, d))
            else:
                btn.clicked.connect(lambda _, h=hour, d=day_col, bl=cell_type: self._register_block(h, d, bl))
        else:
            btn.setStyleSheet(
                f"""
                QPushButton {{
                    background:{color}22; color:{PALETTE['text']};
                    border:1px solid {color}66; border-radius:6px;
                    font-size:11px; font-weight:600;
                }}
                QPushButton:hover {{ background:{color}44; }}
            """
            )
            if cell_type == "EJ":
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.clicked.connect(lambda _, h=hour, d=day_col: self._register_block(h, d, "EJ"))
        return btn

    def _cell_click(self, hour, day_col):
        dlg = AssignBlockDialog(self.data, hour, day_col, self)
        if dlg.exec():
            block_type = dlg.get_type()
            cell_key = f"{hour}_{day_col}"
            self._remove_auto_registro(hour, day_col)
            if block_type == "LIBRE":
                self.data.setdefault("schedule", {}).pop(cell_key, None)
            else:
                self.data.setdefault("schedule", {})[cell_key] = {"type": block_type, "text": BLOQUES.get(block_type, ("", ""))[0]}
                self._sync_auto_registro(hour, day_col, block_type)
            save_data(self.data)
            self._build_table()

    def _register_block(self, hour, day_col, bloque):
        from .dialogs import RegistrarDialog  # import local para evitar fallos por recarga/ciclos
        slot_date = self._slot_date(day_col)
        if slot_date != date.today():
            QMessageBox.information(self, "Registro automático", "Solo se registra automáticamente en el día actual.")
            return
        dlg = RegistrarDialog(
            self.data,
            bloque,
            self,
            fixed_horas=self._slot_hours(hour),
            allow_edit_horas=(bloque == "EJ"),
            default_date=slot_date,
        )
        if dlg.exec():
            reg = dlg.get_registro()
            self.data.setdefault("registros", []).append(reg)
            tags = self.data.setdefault("tags", [])
            for tag in reg.get("tags", []):
                if tag not in tags:
                    tags.append(tag)
            tags.sort(key=str.lower)
            save_data(self.data)
            self.registro_added.emit()

    def refresh(self):
        self._build_table()

    def _slot_hours(self, hour):
        start, end = hour.split("–")
        return max(0.25, float(int(end) - int(start)))

    def _slot_date(self, day_col):
        return self._monday() + timedelta(days=day_col)

    def _remove_auto_registro(self, hour, day_col):
        slot_date = self._slot_date(day_col).isoformat()
        slot_id = f"{slot_date}_{hour}_{day_col}"
        self.data["registros"] = [
            r for r in self.data.get("registros", [])
            if r.get("auto_slot") != slot_id
        ]

    def _sync_auto_registro(self, hour, day_col, block_type):
        settings = self.data.get("settings", {})
        slot_date = self._slot_date(day_col)
        if not settings.get("auto_registro_horario", True):
            return
        if slot_date != date.today():
            return
        slot_id = f"{slot_date.isoformat()}_{hour}_{day_col}"
        self.data.setdefault("registros", []).append(
            {
                "date": slot_date.isoformat(),
                "bloque": block_type,
                "horas": self._slot_hours(hour),
                "subtema": None,
                "nota": f"Auto-horario {hour}",
                "tags": ["Auto"],
                "auto_slot": slot_id,
            }
        )


class RegistroTab(QWidget):
    registro_added = pyqtSignal()

    def __init__(self, data):
        super().__init__()
        self.data = data
        self._build()

    def _build(self):
        lay = QHBoxLayout(self)
        lay.setContentsMargins(16, 16, 16, 16)
        lay.setSpacing(16)

        left = QWidget()
        left.setMaximumWidth(340)
        left_lay = QVBoxLayout(left)
        left_lay.setSpacing(14)

        left_lay.addWidget(Label("Registrar sesión", 16, bold=True))
        left_lay.addWidget(Label("Añade una sesión completada.", 12, PALETTE['muted']))
        left_lay.addWidget(Separator())

        left_lay.addWidget(Label("Inicio rápido:", 12, PALETTE['muted']))
        grid_btns = QGridLayout()
        grid_btns.setSpacing(8)
        bnames = self.data.get("b_nombres", {})
        for i, (k, (def_name, color)) in enumerate(BLOQUES.items()):
            name = bnames.get(k, def_name) if k != "EJ" else "Ejercicio"
            b = QPushButton(f"{k}\n{name}")
            b.setFixedHeight(64)
            b.setStyleSheet(btn_color(color))
            b.clicked.connect(lambda _, bl=k: self._quick_register(bl))
            grid_btns.addWidget(b, i // 2, i % 2)
        left_lay.addLayout(grid_btns)

        left_lay.addWidget(Separator())
        btn_temas = QPushButton("⚙ Administrar temas B1")
        btn_temas.clicked.connect(self._manage_temas)
        left_lay.addWidget(btn_temas)
        btn_tags = QPushButton("🏷️ Administrar etiquetas")
        btn_tags.clicked.connect(self._manage_tags)
        left_lay.addWidget(btn_tags)

        left_lay.addWidget(Label("Renombrar bloques:", 12, PALETTE['muted']))
        self.rename_inputs = {}
        bnames = self.data.get("b_nombres", {})
        for k in ("B1", "B2", "B3", "B4"):
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
        right_lay.addWidget(self.list_w)
        lay.addWidget(right)
        self.refresh()

    def _quick_register(self, bloque):
        from .dialogs import RegistrarDialog  # import local para evitar NameError en algunos entornos
        by_block = self._today_available_hours()
        hours = by_block.get(bloque, 0.0)
        if hours <= 0:
            QMessageBox.warning(self, "Bloque no disponible", "Ese bloque no está disponible en tu horario de hoy.")
            return
        dlg = RegistrarDialog(
            self.data,
            bloque,
            self,
            fixed_horas=hours,
            allow_edit_horas=(bloque == "EJ"),
            default_date=date.today(),
        )
        if dlg.exec():
            reg = dlg.get_registro()
            self.data.setdefault("registros", []).append(reg)
            tags = self.data.setdefault("tags", [])
            for tag in reg.get("tags", []):
                if tag not in tags:
                    tags.append(tag)
            tags.sort(key=str.lower)
            save_data(self.data)
            self.refresh()
            self.registro_added.emit()

    def _today_available_hours(self):
        today_col = date.today().weekday()
        sched = self.data.get("schedule", {})
        by_block = defaultdict(float)
        for hour in HOURS:
            base_type, _ = BASE_SCHEDULE.get(hour, {}).get(today_col, ("LIBRE", ""))
            cell_key = f"{hour}_{today_col}"
            cell_type = sched.get(cell_key, {}).get("type", base_type)
            if cell_type in BLOQUES:
                start, end = hour.split("–")
                by_block[cell_type] += max(0.25, float(int(end) - int(start)))
        return by_block

    def _manage_temas(self):
        TemasB1Dialog(self.data, self).exec()

    def _manage_tags(self):
        TagsDialog(self.data, self).exec()

    def _save_names(self):
        self.data.setdefault("b_nombres", {})
        for k, inp in self.rename_inputs.items():
            self.data["b_nombres"][k] = inp.text().strip() or BLOQUES[k][0]
        save_data(self.data)

    def _delete_selected(self):
        row = self.list_w.currentRow()
        if row < 0:
            return
        idx = self.list_w.currentItem().data(Qt.ItemDataRole.UserRole)
        if idx is not None and QMessageBox.question(self, "Eliminar", "¿Eliminar este registro?") == QMessageBox.StandardButton.Yes:
            self.data["registros"].pop(idx)
            save_data(self.data)
            self.refresh()
            self.registro_added.emit()

    def refresh(self):
        self.list_w.clear()
        registros = self.data.get("registros", [])
        bnames = self.data.get("b_nombres", {})
        temas = {t["id"]: t["nombre"] for t in self.data.get("b1_temas", [])}
        for i, reg in enumerate(reversed(registros)):
            bl = reg["bloque"]
            color = BLOQUES.get(bl, ("?", "#888"))[1]
            name = bnames.get(bl, BLOQUES.get(bl, ("?", ""))[0]) if bl != "EJ" else "Ejercicio"
            subtema = f" › {temas.get(reg['subtema'], '?')}" if reg.get("subtema") else ""
            nota = f" — {reg['nota']}" if reg.get("nota") else ""
            tags = f"  ·  🏷 {', '.join(reg.get('tags', []))}" if reg.get("tags") else ""
            item = QListWidgetItem(f"  {reg['date']}  ·  {bl} {name}{subtema}  ·  {reg['horas']}h{nota}{tags}")
            item.setForeground(QColor(color))
            item.setData(Qt.ItemDataRole.UserRole, len(registros) - 1 - i)
            self.list_w.addItem(item)


class EstadisticasTab(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self._build()
        self.refresh()

    def _build(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(16, 16, 16, 16)
        outer.setSpacing(14)

        top = QHBoxLayout()
        top.addWidget(Label("Período:", 13, PALETTE['muted']))
        self.range_cb = QComboBox()
        self.range_cb.addItems(["Última semana", "Últimos 30 días", "Últimos 90 días", "Todo el tiempo"])
        self.range_cb.currentIndexChanged.connect(self.refresh)
        top.addWidget(self.range_cb)
        top.addWidget(Label("Etiqueta:", 13, PALETTE['muted']))
        self.tag_cb = QComboBox()
        self.tag_cb.addItem("Todas", "__all__")
        self.tag_cb.currentIndexChanged.connect(self.refresh)
        top.addWidget(self.tag_cb)
        top.addStretch()
        outer.addLayout(top)

        self.kpi_row = QHBoxLayout()
        self.kpi_row.setSpacing(10)
        outer.addLayout(self.kpi_row)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        self.charts_lay = QVBoxLayout(container)
        self.charts_lay.setSpacing(16)
        scroll.setWidget(container)
        outer.addWidget(scroll)

    def _date_limit(self):
        idx = self.range_cb.currentIndex()
        if idx == 0:
            return date.today() - timedelta(days=7)
        if idx == 1:
            return date.today() - timedelta(days=30)
        if idx == 2:
            return date.today() - timedelta(days=90)
        return date(2000, 1, 1)

    def refresh(self):
        self._clear_kpis()
        self._clear_charts()
        self._reload_tag_filter()
        filtered = self._filtered_records()
        temas = {t["id"]: t["nombre"] for t in self.data.get("b1_temas", [])}
        bnames = self.data.get("b_nombres", {})
        by_block, by_tag = self._aggregate_stats(filtered)

        self._render_kpis(filtered, by_block)
        if not filtered:
            self.charts_lay.addWidget(Label("Sin datos para el período seleccionado.", 13, PALETTE['muted'], italic=True))
            return

        self._render_block_hours(by_block, bnames)
        self._render_cumulative_progress(filtered, bnames)
        self._render_time_distribution(by_block, bnames)
        if by_tag:
            self._render_tag_hours(by_tag)
        self._render_b1_topics(filtered, temas)
        self._render_weekday_activity(filtered)
        self._render_weekly_hours(filtered)
        self.charts_lay.addStretch()

    def _filtered_records(self):
        filtered = []
        selected_tag = self.tag_cb.currentData() if hasattr(self, "tag_cb") else "__all__"
        for r in self.data.get("registros", []):
            try:
                d = datetime.strptime(r["date"], "%Y-%m-%d").date()
                if d >= self._date_limit():
                    if selected_tag != "__all__" and selected_tag not in r.get("tags", []):
                        continue
                    filtered.append((d, r))
            except Exception:
                continue
        return filtered

    def _reload_tag_filter(self):
        if not hasattr(self, "tag_cb"):
            return
        current = self.tag_cb.currentData()
        tags = sorted({tag for r in self.data.get("registros", []) for tag in r.get("tags", [])}, key=str.lower)
        self.tag_cb.blockSignals(True)
        self.tag_cb.clear()
        self.tag_cb.addItem("Todas", "__all__")
        for tag in tags:
            self.tag_cb.addItem(tag, tag)
        if current:
            idx = self.tag_cb.findData(current)
            self.tag_cb.setCurrentIndex(idx if idx >= 0 else 0)
        self.tag_cb.blockSignals(False)

    def _aggregate_stats(self, filtered):
        by_block = defaultdict(float)
        by_tag = defaultdict(float)
        for _, r in filtered:
            if r.get("bloque") not in BLOQUES:
                continue
            by_block[r["bloque"]] += r["horas"]
            tags = r.get("tags", [])
            if tags:
                share = r["horas"] / len(tags)
                for tag in tags:
                    by_tag[tag] += share
        return by_block, by_tag

    def _render_kpis(self, filtered, by_block):
        for label, val, color in [
            ("Total horas", f"{sum(r['horas'] for _, r in filtered):.1f}h", PALETTE['text']),
            ("B1 Aprendizaje", f"{by_block['B1']:.1f}h", PALETTE['B1']),
            ("B2 Práctica", f"{by_block['B2']:.1f}h", PALETTE['B2']),
            ("B3 Proyecto", f"{by_block['B3']:.1f}h", PALETTE['B3']),
            ("B4 Investigación", f"{by_block['B4']:.1f}h", PALETTE['B4']),
            ("Ejercicio", f"{by_block['EJ']:.1f}h", PALETTE['EJ']),
            ("Sesiones", str(len(filtered)), PALETTE['muted']),
        ]:
            card = KpiCard(label, val, color)
            card.setMinimumWidth(110)
            self.kpi_row.addWidget(card)

    def _render_block_hours(self, by_block, bnames):
        self._add_section_label("Horas por bloque")
        canvas1 = MplCanvas(8, 3.2)
        ax = canvas1.fig.add_subplot(111)
        blocks = [b for b in BLOQUES if by_block[b] > 0]
        colors = [BLOQUES[b][1] for b in blocks]
        values = [by_block[b] for b in blocks]
        labels = [bnames.get(b, BLOQUES[b][0]) if b != "EJ" else "Ejercicio" for b in blocks]
        bars = ax.bar(labels, values, color=[c + "cc" for c in colors], width=0.5, edgecolor=colors, linewidth=1.2)
        for bar, v in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05, f"{v:.1f}h", ha="center", va="bottom", color=PALETTE['text'], fontsize=10, fontweight="600")
        self._style_axes(ax, ylabel="Horas")
        canvas1.fig.tight_layout()
        self.charts_lay.addWidget(canvas1)

    def _render_cumulative_progress(self, filtered, bnames):
        self._add_section_label("Progreso acumulado en el tiempo")
        canvas2 = MplCanvas(8, 3.2)
        ax2 = canvas2.fig.add_subplot(111)
        by_date = defaultdict(lambda: defaultdict(float))
        for d, r in sorted(filtered, key=lambda x: x[0]):
            by_date[d][r["bloque"]] += r["horas"]
        for bl, color in [(b, BLOQUES[b][1]) for b in BLOQUES]:
            all_dates = sorted(by_date.keys())
            daily = [by_date[d].get(bl, 0) for d in all_dates]
            cumul = list(np.cumsum(daily))
            if any(v > 0 for v in cumul):
                name = bnames.get(bl, BLOQUES[bl][0]) if bl != "EJ" else "Ejercicio"
                ax2.plot(all_dates, cumul, color=color, linewidth=2.5, label=name, marker="o", markersize=4)
                ax2.fill_between(all_dates, cumul, alpha=0.08, color=color)
        ax2.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
        self._style_axes(ax2, ylabel="Horas acumuladas")
        ax2.legend(fontsize=9, facecolor=PALETTE['surface2'], labelcolor=PALETTE['text'], edgecolor=PALETTE['border'])
        canvas2.fig.tight_layout()
        self.charts_lay.addWidget(canvas2)

    def _render_time_distribution(self, by_block, bnames):
        self._add_section_label("Distribución de tiempo")
        canvas3 = MplCanvas(6, 3.5)
        ax3 = canvas3.fig.add_subplot(111)
        ax3.set_facecolor(PALETTE["surface"])
        if any(by_block[b] > 0 for b in BLOQUES):
            sizes = [by_block[b] for b in BLOQUES if by_block[b] > 0]
            clrs = [BLOQUES[b][1] for b in BLOQUES if by_block[b] > 0]
            lbls = [bnames.get(b, BLOQUES[b][0]) if b != "EJ" else "Ejercicio" for b in BLOQUES if by_block[b] > 0]
            wedges, texts, autotexts = ax3.pie(
                sizes,
                labels=lbls,
                colors=[c + "cc" for c in clrs],
                autopct="%1.1f%%",
                pctdistance=0.75,
                wedgeprops=dict(width=0.55, edgecolor=PALETTE["surface"], linewidth=2),
            )
            for t in texts:
                t.set_color(PALETTE["muted"])
                t.set_fontsize(9)
            for at in autotexts:
                at.set_color(PALETTE["text"])
                at.set_fontsize(9)
                at.set_fontweight("bold")
        canvas3.fig.tight_layout()
        self.charts_lay.addWidget(canvas3)

    def _render_tag_hours(self, by_tag):
        self._add_section_label("Horas por etiqueta")
        canvas_tags = MplCanvas(8, 3.0)
        ax_tags = canvas_tags.fig.add_subplot(111)
        top_items = sorted(by_tag.items(), key=lambda x: -x[1])[:10]
        tag_names = [k for k, _ in top_items]
        tag_vals = [v for _, v in top_items]
        bars_t = ax_tags.barh(tag_names, tag_vals, color=PALETTE["B2"] + "bb", edgecolor=PALETTE["B2"], linewidth=1.0, height=0.55)
        for bar, v in zip(bars_t, tag_vals):
            ax_tags.text(v + 0.03, bar.get_y() + bar.get_height() / 2, f"{v:.1f}h", va="center", color=PALETTE["text"], fontsize=9)
        self._style_axes(ax_tags, xlabel="Horas")
        ax_tags.invert_yaxis()
        canvas_tags.fig.tight_layout()
        self.charts_lay.addWidget(canvas_tags)

    def _render_b1_topics(self, filtered, temas):
        b1_recs = [(d, r) for d, r in filtered if r["bloque"] == "B1" and r.get("subtema")]
        if b1_recs:
            self._add_section_label("B1 — Horas por subtema de aprendizaje")
            canvas4 = MplCanvas(8, 3.0)
            ax4 = canvas4.fig.add_subplot(111)
            by_tema = defaultdict(float)
            for _, r in b1_recs:
                by_tema[temas.get(r["subtema"], "?")] += r["horas"]
            items = sorted(by_tema.items(), key=lambda x: -x[1])
            names, vals = [i[0] for i in items], [i[1] for i in items]
            bars4 = ax4.barh(names, vals, color=[PALETTE['B1'] + "cc"] * len(names), edgecolor=PALETTE['B1'], linewidth=1.0, height=0.5)
            for bar, v in zip(bars4, vals):
                ax4.text(v + 0.05, bar.get_y() + bar.get_height() / 2, f"{v:.1f}h", va="center", color=PALETTE['text'], fontsize=10, fontweight="600")
            self._style_axes(ax4, xlabel="Horas")
            ax4.invert_yaxis()
            canvas4.fig.tight_layout()
            self.charts_lay.addWidget(canvas4)

    def _render_weekday_activity(self, filtered):
        self._add_section_label("Actividad por día de la semana")
        canvas5 = MplCanvas(8, 2.8)
        ax5 = canvas5.fig.add_subplot(111)
        day_hrs = defaultdict(float)
        for d, r in filtered:
            day_hrs[d.weekday()] += r["horas"]
        hvals = [day_hrs[d] for d in range(7)]
        max_val = max(hvals) if hvals else 0
        bar_colors = [PALETTE["B1"] + "cc" if v == max_val else PALETTE["surface3"] for v in hvals]
        bars5 = ax5.bar([d[:3] for d in DAYS_ES], hvals, color=bar_colors, edgecolor=[PALETTE["B1"] if v == max_val else PALETTE["border"] for v in hvals], linewidth=1.0, width=0.6)
        for bar, v in zip(bars5, hvals):
            if v > 0:
                ax5.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.05, f"{v:.0f}h", ha="center", va="bottom", color=PALETTE["text"], fontsize=9)
        self._style_axes(ax5, ylabel="Horas")
        canvas5.fig.tight_layout()
        self.charts_lay.addWidget(canvas5)

    def _render_weekly_hours(self, filtered):
        self._add_section_label("Horas por semana (últimas 12 semanas)")
        canvas6 = MplCanvas(8, 2.8)
        ax6 = canvas6.fig.add_subplot(111)
        week_hrs = defaultdict(float)
        for d, r in filtered:
            week_start = d - timedelta(days=d.weekday())
            week_hrs[week_start] += r["horas"]
        if week_hrs:
            weeks = sorted(week_hrs.keys())[-12:]
            wvals = [week_hrs[w] for w in weeks]
            wlbls = [w.strftime("%d/%m") for w in weeks]
            max_w = max(wvals)
            ax6.bar(wlbls, wvals, color=[PALETTE["EJ"] + "cc" if v == max_w else PALETTE["surface3"] for v in wvals], edgecolor=[PALETTE["EJ"] if v == max_w else PALETTE["border"] for v in wvals], linewidth=1.0, width=0.6)
            ax6.tick_params(axis="x", rotation=30, colors=PALETTE["muted"], labelsize=9)
        self._style_axes(ax6, ylabel="Horas")
        canvas6.fig.tight_layout()
        self.charts_lay.addWidget(canvas6)

    def _style_axes(self, ax, xlabel=None, ylabel=None):
        ax.set_facecolor(PALETTE['surface'])
        if xlabel:
            ax.set_xlabel(xlabel, color=PALETTE['muted'], fontsize=10)
        if ylabel:
            ax.set_ylabel(ylabel, color=PALETTE['muted'], fontsize=10)
        ax.tick_params(colors=PALETTE['muted'])
        for sp in ax.spines.values():
            sp.set_color(PALETTE['border'])

    def _add_section_label(self, text):
        lbl = Label(text, 13, PALETTE['muted'], bold=True)
        lbl.setStyleSheet(f"color:{PALETTE['muted']}; font-size:12px; font-weight:600; border-bottom:1px solid {PALETTE['border']}; padding-bottom:4px; margin-top:8px;")
        self.charts_lay.addWidget(lbl)

    def _clear_kpis(self):
        while self.kpi_row.count():
            item = self.kpi_row.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _clear_charts(self):
        while self.charts_lay.count():
            item = self.charts_lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
