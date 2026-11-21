"""Tests de tareas.py. Ejecútalos con: python -m pytest

Estos tests de agregar() son el modelo: un test por cada regla del docstring.
Escribe los de completar(), eliminar() y editar() con el mismo estilo,
antes de implementar cada función.
"""

import pytest

from tareas import agregar, completar, editar, eliminar


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


def test_completar_devuelve_la_tarea_y_la_marca_como_hecha():
    tareas = [
        {"id": 1, "titulo": "Estudiar", "hecha": False},
        {"id": 2, "titulo": "Leer", "hecha": False},
    ]
    tarea = completar(tareas, 2)
    assert tarea == {"id": 2, "titulo": "Leer", "hecha": True}
    assert tareas[1] == tarea
    assert tareas[0] == {"id": 1, "titulo": "Estudiar", "hecha": False}


def test_completar_id_inexistente_da_error():
    tareas = [
        {"id": 1, "titulo": "Estudiar", "hecha": False},
        {"id": 2, "titulo": "Leer", "hecha": False},
    ]
    with pytest.raises(ValueError, match="No existe la tarea 7"):
        completar(tareas, 7)
    assert tareas == [
        {"id": 1, "titulo": "Estudiar", "hecha": False},
        {"id": 2, "titulo": "Leer", "hecha": False},
    ]


def test_completar_tarea_ya_hecha_sigue_hecha():
    tareas = [{"id": 1, "titulo": "Estudiar", "hecha": True}]
    tarea = completar(tareas, 1)
    assert tarea["hecha"] is True
    assert tareas[0]["hecha"] is True


def test_eliminar_devuelve_la_tarea_y_la_quita_de_la_lista():
    tareas = [
        {"id": 1, "titulo": "Estudiar", "hecha": False},
        {"id": 2, "titulo": "Leer", "hecha": False},
        {"id": 3, "titulo": "Practicar", "hecha": True},
    ]
    tarea = eliminar(tareas, 2)
    assert tarea == {"id": 2, "titulo": "Leer", "hecha": False}
    assert [t["id"] for t in tareas] == [1, 3]
    assert len(tareas) == 2


def test_eliminar_id_inexistente_da_error():
    tareas = [
        {"id": 1, "titulo": "Estudiar", "hecha": False},
        {"id": 2, "titulo": "Leer", "hecha": False},
    ]
    with pytest.raises(ValueError, match="No existe la tarea 7"):
        eliminar(tareas, 7)
    assert tareas == [
        {"id": 1, "titulo": "Estudiar", "hecha": False},
        {"id": 2, "titulo": "Leer", "hecha": False},
    ]


def test_eliminar_no_cambia_los_ids_de_las_demas():
    tareas = [
        {"id": 1, "titulo": "Estudiar", "hecha": False},
        {"id": 5, "titulo": "Leer", "hecha": False},
        {"id": 9, "titulo": "Practicar", "hecha": False},
    ]
    eliminar(tareas, 5)
    assert [t["id"] for t in tareas] == [1, 9]


def test_editar_devuelve_la_tarea_y_cambia_el_titulo():
    tareas = [
        {"id": 1, "titulo": "Estudiar", "hecha": False},
        {"id": 2, "titulo": "Leer", "hecha": False},
    ]
    tarea = editar(tareas, 2, "Practicar")
    assert tarea == {"id": 2, "titulo": "Practicar", "hecha": False}
    assert tareas[1] == tarea
    assert tareas[0] == {"id": 1, "titulo": "Estudiar", "hecha": False}


def test_editar_quita_los_espacios_de_los_extremos():
    tareas = [{"id": 1, "titulo": "Estudiar", "hecha": False}]
    tarea = editar(tareas, 1, "   Leer   ")
    assert tarea["titulo"] == "Leer"


def test_editar_titulo_vacio_da_error():
    tareas = [{"id": 1, "titulo": "Estudiar", "hecha": False}]
    with pytest.raises(ValueError, match="El título no puede estar vacío"):
        editar(tareas, 1, "    ")
    assert tareas == [{"id": 1, "titulo": "Estudiar", "hecha": False}]


def test_editar_acepta_un_titulo_de_80_caracteres():
    tareas = [{"id": 1, "titulo": "Estudiar", "hecha": False}]
    tarea = editar(tareas, 1, "a" * 80)
    assert tarea["titulo"] == "a" * 80


def test_editar_titulo_de_81_caracteres_da_error():
    tareas = [{"id": 1, "titulo": "Estudiar", "hecha": False}]
    with pytest.raises(ValueError, match="El título no puede superar 80 caracteres"):
        editar(tareas, 1, "a" * 81)
    assert tareas == [{"id": 1, "titulo": "Estudiar", "hecha": False}]


def test_editar_id_inexistente_da_error():
    tareas = [{"id": 1, "titulo": "Estudiar", "hecha": False}]
    with pytest.raises(ValueError, match="No existe la tarea 7"):
        editar(tareas, 7, "Leer")
    assert tareas == [{"id": 1, "titulo": "Estudiar", "hecha": False}]


def test_editar_no_cambia_si_la_tarea_esta_hecha():
    tareas = [
        {"id": 1, "titulo": "Estudiar", "hecha": True},
        {"id": 2, "titulo": "Leer", "hecha": False},
    ]
    hecha = editar(tareas, 1, "Repasar")
    pendiente = editar(tareas, 2, "Practicar")
    assert hecha["hecha"] is True
    assert pendiente["hecha"] is False
