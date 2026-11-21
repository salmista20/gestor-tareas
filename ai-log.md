# Bitácora de IA

Esta bitácora registra cómo trabajaste con el agente durante el laboratorio: qué le pediste, qué propuso, qué decidiste y cómo lo comprobaste. No se evalúa cuánto código escribió la IA, sino tu criterio: por qué aceptaste, rechazaste o ajustaste cada propuesta. Agrega una entrada por cada paso del laboratorio y otra cada vez que deshagas un cambio del agente.

## Plantilla

Copia este bloque para cada entrada nueva:

```markdown
### Entrada N

- **Fecha:** AAAA-MM-DD
- **Paso del laboratorio:** (por ejemplo: memoria del proyecto, plan, RED de completar, GREEN de completar, refactor)
- **Prompt clave (literal):**
  > Pega aquí el prompt exacto que usaste.
- **Qué propuso el agente:** resumen en una o dos líneas.
- **Decisión:** aceptado / rechazado / ajustado. Por qué: ...
- **Cómo lo verifiqué:** tests (`python -m pytest`), navegador (`python servidor.py`), lectura del cambio...
```

## Ejemplo

### Entrada 1

- **Fecha:** el día del laboratorio
- **Paso del laboratorio:** memoria del proyecto (`/init`)
- **Prompt clave (literal):**
  > /init
- **Qué propuso el agente:** creó `AGENTS.md` con un resumen del proyecto, cómo ejecutarlo y una descripción de los archivos.
- **Decisión:** ajustado. Quité la descripción archivo por archivo, porque el agente la puede deducir leyendo el código. Agregué lo que no puede adivinar: que `servidor.py` y `almacen.py` no se modifican, que los mensajes de error deben ser exactamente los del docstring y que nunca se cambia un test solo para que pase.
- **Cómo lo verifiqué:** leí el archivo completo antes de guardarlo y comprobé que los comandos que menciona funcionan: `python -m pytest` pasa los tests de `agregar` y `python servidor.py` abre la página.

## Entradas de la sesión

### Entrada 2

- **Fecha:** 2026-11-21
- **Paso del laboratorio:** memoria del proyecto (`AGENTS.md`)
- **Prompt clave (literal):**
  > instala agents.MD
- **Qué propuso el agente:** creó `AGENTS.md` en la raíz con los comandos `python -m pytest` y `python servidor.py`, las restricciones de archivos y dependencias, el contrato de mensajes de error y el flujo TDD.
- **Decisión:** aceptado. No incluyó descripción archivo por archivo ni consejos genéricos, porque se deducen leyendo el código; sí incluyó lo que no se puede adivinar: no tocar `servidor.py` ni `almacen.py`, no añadir dependencias, mensajes de error exactos de los docstrings y no cambiar tests para que pasen.
- **Cómo lo verifiqué:** leí el archivo y comprobé los comandos en la máquina: `python -m pytest` da 8 tests en verde. Instalé Python 3.12, pytest y Git porque no estaban disponibles; luego hice `git init` y el commit base.

### Entrada 3

- **Fecha:** 2026-11-21
- **Paso del laboratorio:** RED y GREEN de `completar`
- **Prompt clave (literal):**
  > LA TAREA ES EJECUTAR LOS PASOS DEL ARCHIVO TAREAS.PY
- **Qué propuso el agente:** escribió tres tests (devuelve y marca la tarea, id inexistente, tarea ya hecha) sin tocar `tareas.py`, y después implementó la función con búsqueda por id y `ValueError` exacto.
- **Decisión:** aceptado. Un test por cada regla del docstring, con el estilo de los tests de `agregar`; la implementación no cambió mensajes de error ni modificó tests.
- **Cómo lo verifiqué:** en RED, los 3 tests nuevos fallaron con `NotImplementedError` y los 8 anteriores pasaron; en GREEN, `python -m pytest` da 11 tests en verde.

### Entrada 4

- **Fecha:** 2026-11-21
- **Paso del laboratorio:** RED y GREEN de `eliminar`
- **Prompt clave (literal):**
  > LA TAREA ES EJECUTAR LOS PASOS DEL ARCHIVO TAREAS.PY
- **Qué propuso el agente:** tres tests (devuelve y quita la tarea, id inexistente, los demás ids no cambian) y una implementación con `enumerate`/`pop` y el `ValueError` del docstring.
- **Decisión:** aceptado. `pop` elimina sin renumerar, así que se cumple la regla de conservar los ids; no se tocaron los tests ni los mensajes de error.
- **Cómo lo verifiqué:** RED con 3 fallos por `NotImplementedError` (11 tests seguían en verde); GREEN con `python -m pytest`: 14 tests en verde.
