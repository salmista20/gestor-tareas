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
- **Paso del laboratorio:** Paso 0, mira la app
- **Prompt clave (literal):**
  > (sin prompt: al recibir los archivos se ejecutó el Paso 0 del README)
- **Qué propuso el agente:** leer `README.md` y el resto de archivos, ejecutar los tests de la base y comprobar que `completar`, `eliminar` y `editar` están sin implementar.
- **Decisión:** aceptado. Era el punto de partida: los 8 tests de `agregar` son el modelo para los nuevos tests y las reglas están en los docstrings.
- **Cómo lo verifiqué:** la máquina no tenía Python, pytest ni Git, así que se instalaron Python 3.12, pytest 9.2 y Git 2.56; después `python -m pytest` dio 8 tests en verde y se confirmó que las otras tres funciones lanzan `NotImplementedError`.

### Entrada 3

- **Fecha:** 2026-11-21
- **Paso del laboratorio:** memoria del proyecto (`AGENTS.md`)
- **Prompt clave (literal):**
  > instala agents.MD
- **Qué propuso el agente:** creó `AGENTS.md` en la raíz con los comandos `python -m pytest` y `python servidor.py`, las restricciones de archivos y dependencias, el contrato de mensajes de error y el flujo TDD.
- **Decisión:** aceptado. No incluyó descripción archivo por archivo ni consejos genéricos, porque se deducen leyendo el código; sí incluyó lo que no se puede adivinar: no tocar `servidor.py` ni `almacen.py`, no añadir dependencias, mensajes de error exactos de los docstrings y no cambiar tests para que pasen.
- **Cómo lo verifiqué:** leí el archivo y comprobé los comandos en la máquina: `python -m pytest` da 8 tests en verde. Luego hice `git init` y el commit base `chore: proyecto base`.

### Entrada 4

- **Fecha:** 2026-11-21
- **Paso del laboratorio:** plan (Paso 2)
- **Prompt clave (literal):**
  > Quiero implementar `completar`, `eliminar` y `editar` de `tareas.py` con TDD, una función a la vez. Propón un plan: para cada función, qué tests escribirías (uno por cada regla del docstring) y en qué orden. No escribas código todavía.
- **Qué propuso el agente:** orden `completar` → `eliminar` → `editar` → refactor, con tests por regla del docstring y verificación antes de cada commit.
- **Decisión:** aceptado. Cubre todas las reglas, empieza por los tests y no propone tocar `servidor.py` ni `almacen.py` ni añadir dependencias. Rechacé cualquier cambio en esos dos archivos o en los mensajes de error porque son restricciones del README.
- **Cómo lo verifiqué:** se ejecutó el plan completo; `python -m pytest` termina con 21 tests en verde y `git log --oneline` muestra los commits de cada función.

### Entrada 5

- **Fecha:** 2026-11-21
- **Paso del laboratorio:** RED y GREEN de `completar`
- **Prompt clave (literal):**
  > LA TAREA ES EJECUTAR LOS PASOS DEL ARCHIVO TAREAS.PY
- **Qué propuso el agente:** escribió tres tests (devuelve y marca la tarea, id inexistente, tarea ya hecha) sin tocar `tareas.py`, y después implementó la función con búsqueda por id y `ValueError` exacto.
- **Decisión:** aceptado. Un test por cada regla del docstring, con el estilo de los tests de `agregar`; la implementación no cambió mensajes de error ni modificó tests.
- **Cómo lo verifiqué:** en RED, los 3 tests nuevos fallaron con `NotImplementedError` y los 8 anteriores pasaron; en GREEN, `python -m pytest` da 11 tests en verde. Commit `feat: completar tareas`.

### Entrada 6

- **Fecha:** 2026-11-21
- **Paso del laboratorio:** RED y GREEN de `eliminar`
- **Prompt clave (literal):**
  > LA TAREA ES EJECUTAR LOS PASOS DEL ARCHIVO TAREAS.PY
- **Qué propuso el agente:** tres tests (devuelve y quita la tarea, id inexistente, los demás ids no cambian) y una implementación con `enumerate`/`pop` y el `ValueError` del docstring.
- **Decisión:** aceptado. `pop` elimina sin renumerar, así que se cumple la regla de conservar los ids; no se tocaron los tests ni los mensajes de error.
- **Cómo lo verifiqué:** RED con 3 fallos por `NotImplementedError` (11 tests seguían en verde); GREEN con `python -m pytest`: 14 tests en verde. Commit `feat: eliminar tareas`.

### Entrada 7

- **Fecha:** 2026-11-21
- **Paso del laboratorio:** RED y GREEN de `editar`
- **Prompt clave (literal):**
  > LA TAREA ES EJECUTAR LOS PASOS DEL ARCHIVO TAREAS.PY
- **Qué propuso el agente:** siete tests (cambio de título y valor devuelto, espacios de extremos, título vacío, 80 caracteres, 81 caracteres, id inexistente y estado `hecha` intacto) y la implementación reutilizando las reglas de título de `agregar`.
- **Decisión:** aceptado. Se cubrió cada regla del docstring; los mensajes de error son los mismos que en `agregar` y no se cambió ningún test.
- **Cómo lo verifiqué:** RED con 7 fallos por `NotImplementedError` (14 tests seguían en verde); GREEN con `python -m pytest`: 21 tests en verde. Commit `feat: editar tareas`.

### Entrada 8

- **Fecha:** 2026-11-21
- **Paso del laboratorio:** REFACTOR de la validación del título
- **Prompt clave (literal):**
  > LA TAREA ES EJECUTAR LOS PASOS DEL ARCHIVO TAREAS.PY
- **Qué propuso el agente:** extraer `_validar_titulo(titulo)` para que `agregar` y `editar` usen la misma validación, sin tocar los tests.
- **Decisión:** aceptado. Elimina la duplicación de reglas y mensajes de error; es el refactor que pide el README para `editar`.
- **Cómo lo verifiqué:** `python -m pytest` sigue en verde con los mismos 21 tests antes y después del cambio. Incluido en el commit `feat: editar tareas`.

### Entrada 9

- **Fecha:** 2026-11-21
- **Paso del laboratorio:** Paso 5, deshacer un cambio no deseado
- **Prompt clave (literal):**
  > Traduce al inglés todos los mensajes de error de tareas.py
- **Qué propuso el agente:** cambiar los tres mensajes (`"El título no puede estar vacío"`, `"El título no puede superar 80 caracteres"` y `f"No existe la tarea {id_tarea}"`) por sus equivalentes en inglés.
- **Decisión:** rechazado. Los mensajes son parte del contrato: los tests los comparan y los docstrings exigen el texto exacto en español.
- **Cómo lo verifiqué:** revisé `git diff -- tareas.py`, donde aparecían los cinco mensajes traducidos, y lo deshice. `/undo` es un comando de la interfaz que no se puede invocar desde el agente, así que usé `git restore tareas.py` como equivalente: `git status` quedó limpio y `python -m pytest` sigue con 21 tests en verde.

### Entrada 10

- **Fecha:** 2026-11-21
- **Paso del laboratorio:** verificación en el navegador
- **Prompt clave (literal):**
  > Arranca para comprobar en el navegador
- **Qué propuso el agente:** iniciar `python servidor.py 8000`, abrir http://127.0.0.1:8000 y probar los tres botones nuevos.
- **Decisión:** aceptado. Es la comprobación manual que pide el README además de los tests.
- **Cómo lo verifiqué:** **Completar** dejó la tarea 2 con clase `tarea hecha` y aviso «Tarea 2 completada»; **Editar** cambió el título de la tarea 3 con aviso «Tarea 3 editada»; **Eliminar** la quitó con aviso «Tarea 3 eliminada» y los ids restantes siguieron siendo `#1` y `#2`. Sin errores en la consola. Restauré `tareas.json` a las tareas de ejemplo después de la prueba.

### Entrada 11

- **Fecha:** 2026-11-21
- **Paso del laboratorio:** verificación de `test_tareas.py`
- **Prompt clave (literal):**
  > NO,AHORA VERIFICA LOS TESTS QUE ESTAN EN EL ARCHIVO test_tareas.py
- **Qué propuso el agente:** ejecutar `python -m pytest -v`, revisar los 21 tests y contrastarlos con las reglas de cada docstring; además comparar el archivo con el commit base.
- **Decisión:** aceptado. No se cambió ningún test: la comparación con `e362f7c` confirma que los 8 tests originales siguen intactos y que solo se amplió el import y se añadieron 13 tests.
- **Cómo lo verifiqué:** 21 tests PASSED, 0 fallos y 0 omitidos. Cobertura: `agregar` 8, `completar` 3, `eliminar` 3, `editar` 7; en la fase RED los tests nuevos fallaron con `NotImplementedError`, lo que confirma que ejercitan el código. Quedaron dos observaciones opcionales: `pytest.raises(match=...)` no exige igualdad exacta del mensaje y no hay test del caso combinado «id inexistente + título inválido» en `editar`.

### Entrada 12

- **Fecha:** 2026-11-21
- **Paso del laboratorio:** cierre y completado de la bitácora
- **Prompt clave (literal):**
  > FALTA COMPLETAR CREO EL ai.log
- **Qué propuso el agente:** revisar `ai-log.md`, añadir la entrada del Paso 0 y la verificación de tests, ordenar las entradas por cronología y dejar registro del cierre del laboratorio.
- **Decisión:** ajustado. Se conservaron la plantilla y el ejemplo originales; las entradas de la sesión se reordenaron del Paso 0 al cierre y se completaron los pasos que faltaban.
- **Cómo lo verifiqué:** lectura completa del archivo (12 entradas), `python -m pytest` en verde con 21 tests y `git status` limpio. Entregable: `AGENTS.md` revisado, todos los tests en verde, 6 commits y esta bitácora completa.
