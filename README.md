# Panel de Productividad (PyQt6 + JSON)

Aplicación de escritorio para planificar y registrar sesiones de estudio/productividad con interfaz en **PyQt6** y persistencia local en **JSON**.

## Características

- **Horario semanal visual** con bloques fijos (clases, ejercicio, lectura, etc.).
- **Asignación de bloques libres** (B1, B2, B3, B4, EJ) directamente en la grilla.
- **Registro rápido de sesiones** con fecha, horas, nota y subtema (para B1).
- **Etiquetas (tags) por sesión** para clasificar por área (ej: Programación, Álgebra lineal, FreeCAD).
- **Gestión de temas B1** (crear/eliminar subtemas de aprendizaje).
- **Gestión de etiquetas** desde la interfaz.
- **Renombrado de bloques** B1–B4.
- **Panel de estadísticas** con KPIs y gráficos:
  - Horas por bloque.
  - Horas por etiqueta.
  - Progreso acumulado en el tiempo.
  - Distribución de tiempo.
  - B1 por subtema.
  - Actividad por día de semana.
  - Horas por semana.

## Requisitos

- Python 3.10+
- Dependencias:

```bash
pip install PyQt6 matplotlib numpy
```

## Ejecución

Desde la raíz del proyecto:

```bash
python productividad.py
```

### Modo de color

Puedes ejecutar la app en tema oscuro (por defecto) o claro mediante la variable de entorno `PRODUCTIVIDAD_THEME`:

```bash
PRODUCTIVIDAD_THEME=dark python productividad.py
PRODUCTIVIDAD_THEME=light python productividad.py
```

## Estructura del proyecto

```text
.
├── productividad.py        # Entrypoint (wrapper)
├── app/
│   ├── __init__.py
│   ├── app.py              # Bootstrap de QApplication
│   ├── main_window.py      # Ventana principal y tabs
│   ├── tabs.py             # Horario, Registro, Estadísticas
│   ├── dialogs.py          # Diálogos reutilizables
│   ├── widgets.py          # Componentes UI reutilizables
│   ├── styles.py           # Estilos globales y helpers visuales
│   ├── data.py             # Carga/guardado de datos JSON
│   └── constants.py        # Paleta, bloques, horarios base
└── productividad_data.json # Se crea automáticamente al usar la app
```

## Datos y persistencia

La aplicación guarda información en `productividad_data.json` (en la raíz del proyecto), incluyendo:

> Si el archivo no existe, la app inicia con **datos de prueba** para facilitar validación visual y de gráficas.

- `registros`: sesiones registradas.
- `b1_temas`: catálogo de subtemas de B1.
- `tags`: catálogo de etiquetas sugeridas.
- `schedule`: sobrescrituras del horario base.
- `b_nombres`: nombres personalizados de bloques.

## Desarrollo

Chequeo rápido de sintaxis:

```bash
python -m py_compile productividad.py app/*.py
```

---

Si quieres, también puedo añadir una sección de **capturas**, **roadmap** o **contribución** en este README.
