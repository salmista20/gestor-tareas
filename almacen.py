"""Guarda y carga la lista de tareas en tareas.json.

Este archivo viene listo: no necesitas modificarlo.
"""

import json
from pathlib import Path

RUTA = Path(__file__).resolve().parent / "tareas.json"


def cargar(ruta=RUTA):
    """Devuelve la lista de tareas guardada (lista vacía si no hay archivo)."""
    ruta = Path(ruta)
    if not ruta.exists():
        return []
    return json.loads(ruta.read_text(encoding="utf-8"))


def guardar(tareas, ruta=RUTA):
    """Guarda la lista de tareas en formato JSON."""
    texto = json.dumps(tareas, ensure_ascii=False, indent=2)
    Path(ruta).write_text(texto + "\n", encoding="utf-8")
