# Laboratorio S3: gestor de tareas con un agente

Vas a completar un gestor de tareas con OpenCode siguiendo el flujo de un equipo profesional: memoria del proyecto, plan, test primero, implementación, verificación y commit.
Trabajo individual. Lo que se evalúa no es cuánto código escribe el agente, sino cómo lo diriges y cómo compruebas lo que hace.

## Requisitos

- Python 3.10 o superior, con pytest:

  ```
  python -m pip install pytest
  ```

- Git con tu identidad configurada:

  ```
  git config --global user.name "Tu Nombre"
  git config --global user.email "tu@correo.com"
  ```

- OpenCode instalado y conectado a un modelo.

## Los archivos

| Archivo | Qué es |
|---|---|
| `tareas.py` | Las funciones del gestor. `agregar` ya funciona; `completar`, `eliminar` y `editar` están por implementar. Las reglas de cada una están en su docstring. **Aquí trabajas.** |
| `test_tareas.py` | Los tests de `agregar`, que sirven de modelo. **Tus tests van aquí.** |
| `servidor.py` | La vista web local que muestra las tareas en el navegador. No lo modifiques. |
| `almacen.py` | Guarda las tareas en `tareas.json`. No lo modifiques. |
| `ai-log.md` | Tu bitácora de IA: una plantilla y un ejemplo. |
| `.gitignore` | Lo que Git no debe guardar: `tareas.json` y las cachés de Python y pytest. |

## Paso 0: mira la app

```
python -m pytest
```

Los 8 tests de `agregar` pasan. Ahora, en una segunda terminal:

```
python servidor.py
```

Se abre http://127.0.0.1:8000 con tres tareas de ejemplo. Agrega una tarea: funciona. Pulsa **Completar**: aparece un aviso amarillo que dice `completar() aún no está implementada`.

Deja el servidor encendido. Cuando cambies `tareas.py`, basta con recargar la página (F5) para ver el cambio. Si el archivo tiene un error mientras el agente lo edita, la página lo muestra en rojo; no hace falta reiniciar el servidor.

## Paso 1: Git y memoria del proyecto

Primero convierte la carpeta en un repositorio de Git. ¿Por qué antes de abrir el agente? Porque `/undo` de OpenCode restaura los archivos solo dentro de un repositorio de Git.

```
git init
git add .
git commit -m "chore: proyecto base"
```

Abre OpenCode en la carpeta del proyecto:

```
opencode
```

Ejecuta `/init`. El agente lee el proyecto y crea (o actualiza) `AGENTS.md`, la memoria del proyecto. No lo aceptes tal cual: revísalo y corrígelo. Debe:

- [ ] incluir los comandos `python -m pytest` y `python servidor.py`;
- [ ] decir que no se tocan `servidor.py` ni `almacen.py`;
- [ ] prohibir dependencias nuevas;
- [ ] pedir los mensajes de error exactos de los docstrings;
- [ ] prohibir cambiar un test solo para que pase.

Y borra lo que el agente puede deducir leyendo el código: la descripción archivo por archivo y los consejos genéricos.

Guarda la versión revisada y anota en `ai-log.md` qué cambiaste y por qué (la bitácora trae un ejemplo de esta entrada):

```
git add AGENTS.md
git commit -m "docs: AGENTS.md revisado"
```

## Paso 2: plan

Pulsa Shift+Tab para cambiar al agente **Plan** y pide un plan, sin código:

> Quiero implementar `completar`, `eliminar` y `editar` de `tareas.py` con TDD, una función a la vez. Propón un plan: para cada función, qué tests escribirías (uno por cada regla del docstring) y en qué orden. No escribas código todavía.

Critica el plan antes de aceptarlo:

- ¿Cubre cada regla del docstring?
- ¿Empieza por los tests?
- ¿Propone tocar `servidor.py` o agregar dependencias?

Ajústalo con otro prompt si hace falta y anota en `ai-log.md` qué aceptaste, qué rechazaste y por qué.

## Paso 3: RED

Cambia al agente **Build** (Shift+Tab) y pide solo los tests de `completar`, sin implementar la función. También puedes escribirlos tú.

> Escribe en `test_tareas.py` los tests de `completar`, uno por cada regla de su docstring, con el mismo estilo que los tests de `agregar`. No modifiques `tareas.py`.

Ejecútalos sin salir de OpenCode. Si escribes `!` como primer carácter del prompt, lo que sigue se ejecuta como comando de terminal:

```
!python -m pytest
```

Los tests nuevos deben fallar con `NotImplementedError`: eso es RED. Si alguno pasa con la función todavía sin implementar, ese test no prueba lo que crees.

## Paso 4: GREEN

> Implementa `completar` en `tareas.py` para que pasen los tests. No modifiques los tests.

Verifica tú mismo:

- `!python -m pytest` está todo en verde;
- recarga la página y pulsa **Completar**: la tarea aparece tachada en verde.

Revisa el cambio con `git diff` y guarda el test y el código juntos:

```
git add tareas.py test_tareas.py
git commit -m "feat: completar tareas"
```

## Paso 5: deshacer

Pide a propósito un cambio que no quieres:

> Traduce al inglés todos los mensajes de error de tareas.py

Míralo con `git diff` (los mensajes son parte del contrato: los tests los comparan). Deshazlo con `/undo` (o Ctrl+X y luego U) y confirma con `git status` que `tareas.py` ya no aparece como modificado.

Ten en cuenta dos límites: `/undo` no revierte lo que hayan hecho los comandos de terminal, y fuera de un repositorio de Git solo retrocede la conversación. Anota este paso en `ai-log.md`.

## Paso 6: repite

Haz `eliminar` y luego `editar` con el mismo ciclo: tests que fallan, implementación, verificación y un commit por función.

En `editar` aparece el paso REFACTOR: `editar` necesita las mismas reglas de título que `agregar`. Con los tests en verde, pide extraer la validación del título a una sola función que usen las dos, y comprueba que todos los tests sigan en verde antes del commit.

## Comandos útiles de OpenCode

| Comando | Para qué sirve |
|---|---|
| Shift+Tab | Cambiar entre los agentes Plan y Build |
| `@archivo` | Adjuntar un archivo al prompt, por ejemplo `@tareas.py` |
| `!comando` | Ejecutar un comando en la terminal, por ejemplo `!python -m pytest` |
| `/init` | Crear o actualizar `AGENTS.md` |
| `/undo` y `/redo` | Deshacer o rehacer el último cambio (Ctrl+X U / Ctrl+X R) |
| `/compact` | Resumir la sesión cuando se hace larga |

## Restricciones

- No modifiques `servidor.py` ni `almacen.py`.
- Solo la biblioteca estándar de Python (pytest solo para los tests).
- Los mensajes de error deben ser exactamente los de los docstrings.
- Nunca cambies un test para que pase.

## Entregable

Tu repositorio con:

- `AGENTS.md` revisado por ti;
- todos los tests en verde (`python -m pytest`);
- al menos 3 commits (compruébalo con `git log --oneline`);
- `ai-log.md` con los prompts clave, los planes que aceptaste o rechazaste y por qué.

## Problemas frecuentes

| Problema | Solución |
|---|---|
| El puerto 8000 está ocupado | `python servidor.py 8001` y abre http://127.0.0.1:8001 |
| `git commit` pide tu identidad | Ejecuta los dos comandos `git config --global` de los requisitos |
| `No module named pytest` | `python -m pip install pytest` |
| El navegador no se abre | Abre http://127.0.0.1:8000 a mano |
| `/undo` no restauró los archivos | Revisa que ejecutaste `git init` y el primer commit |
