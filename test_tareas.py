"""Tests de tareas.py. Ejecútalos con: python -m pytest

Estos tests de agregar() son el modelo: un test por cada regla del docstring.
Escribe los de completar(), eliminar() y editar() con el mismo estilo,
antes de implementar cada función.
"""

import pytest

from tareas import agregar


def test_agregar_devuelve_la_tarea_y_la_pone_al_final():
    tareas = [{"id": 1, "titulo": "Estudiar", "hecha": False}]
    tarea = agregar(tareas, "Leer")
    assert tarea == {"id": 2, "titulo": "Leer", "hecha": False}
    assert tareas[-1] == tarea
    assert len(tareas) == 2


def test_agregar_quita_los_espacios_de_los_extremos():
    tareas = []
    tarea = agregar(tareas, "   Estudiar para el parcial  ")
    assert tarea["titulo"] == "Estudiar para el parcial"


def test_agregar_titulo_vacio_da_error():
    tareas = []
    with pytest.raises(ValueError, match="El título no puede estar vacío"):
        agregar(tareas, "    ")
    assert tareas == []


def test_agregar_acepta_un_titulo_de_80_caracteres():
    tareas = []
    tarea = agregar(tareas, "a" * 80)
    assert tarea["titulo"] == "a" * 80


def test_agregar_titulo_de_81_caracteres_da_error():
    tareas = []
    with pytest.raises(ValueError, match="El título no puede superar 80 caracteres"):
        agregar(tareas, "a" * 81)
    assert tareas == []


def test_agregar_en_lista_vacia_usa_el_id_1():
    tareas = []
    tarea = agregar(tareas, "Estudiar")
    assert tarea["id"] == 1


def test_agregar_usa_el_id_mas_alto_mas_uno():
    # Las tareas 2, 3 y 4 se eliminaron: el id nuevo no debe repetir ninguno.
    tareas = [
        {"id": 1, "titulo": "Estudiar", "hecha": False},
        {"id": 5, "titulo": "Leer", "hecha": False},
    ]
    tarea = agregar(tareas, "Practicar")
    assert tarea["id"] == 6


def test_agregar_la_tarea_nueva_empieza_sin_hacer():
    tareas = [{"id": 1, "titulo": "Estudiar", "hecha": True}]
    tarea = agregar(tareas, "Leer")
    assert tarea["hecha"] is False
