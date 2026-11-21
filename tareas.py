"""Gestor de tareas: funciones para manejar una lista de tareas.

Cada tarea es un diccionario como este:

    {"id": 1, "titulo": "Estudiar", "hecha": False}

Todas las funciones reciben la lista de tareas, la modifican directamente
y devuelven la tarea afectada.
"""


def agregar(tareas, titulo):
    """Agrega una tarea nueva al final de la lista y la devuelve.

    Reglas:
    - Se quitan los espacios del inicio y del final del título.
    - Si el título queda vacío: ValueError("El título no puede estar vacío").
    - Si el título tiene más de 80 caracteres:
      ValueError("El título no puede superar 80 caracteres").
    - El id es el id más alto de la lista + 1 (1 si la lista está vacía).
    - La tarea nueva empieza con hecha = False.
    """
    titulo = titulo.strip()
    if titulo == "":
        raise ValueError("El título no puede estar vacío")
    if len(titulo) > 80:
        raise ValueError("El título no puede superar 80 caracteres")

    id_mayor = 0
    for tarea in tareas:
        if tarea["id"] > id_mayor:
            id_mayor = tarea["id"]

    tarea_nueva = {"id": id_mayor + 1, "titulo": titulo, "hecha": False}
    tareas.append(tarea_nueva)
    return tarea_nueva


def completar(tareas, id_tarea):
    """Marca la tarea como hecha y la devuelve.

    Reglas:
    - Si no existe una tarea con ese id: ValueError con el mensaje
      "No existe la tarea 7" (con el id que se pidió).
    - Completar una tarea que ya está hecha no es un error: sigue hecha.
    """
    raise NotImplementedError("completar() aún no está implementada")


def eliminar(tareas, id_tarea):
    """Quita la tarea de la lista y la devuelve.

    Reglas:
    - Si no existe una tarea con ese id: ValueError con el mensaje
      "No existe la tarea 7" (con el id que se pidió).
    - Los ids de las demás tareas no cambian.
    """
    raise NotImplementedError("eliminar() aún no está implementada")


def editar(tareas, id_tarea, titulo):
    """Cambia el título de la tarea y la devuelve.

    Reglas:
    - El título nuevo sigue las mismas reglas que en agregar(): se quitan
      los espacios de los extremos y, si queda vacío o tiene más de 80
      caracteres, se lanza el mismo ValueError con el mismo mensaje.
    - Si no existe una tarea con ese id: ValueError con el mensaje
      "No existe la tarea 7" (con el id que se pidió).
    - No cambia si la tarea está hecha o no.
    """
    raise NotImplementedError("editar() aún no está implementada")
