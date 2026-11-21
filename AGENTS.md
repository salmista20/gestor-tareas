# Memoria del proyecto: gestor de tareas

## Comandos

- `python -m pytest` — ejecuta los tests. Todos deben pasar antes de dar por terminado un cambio.
- `python servidor.py` — abre la vista web en http://127.0.0.1:8000. Si el puerto está ocupado: `python servidor.py 8001`.

## Restricciones

- No modificar `servidor.py` ni `almacen.py`.
- No añadir dependencias nuevas. Solo biblioteca estándar de Python; pytest únicamente en los tests.
- Los mensajes de error deben ser exactamente los que indican los docstrings de `tareas.py` (incluidos acentos y puntuación). Son parte del contrato y los tests los comparan.
- Nunca cambiar un test para que pase. Si un test falla, ajustar la implementación.

## Flujo de trabajo

- Implementar una función a la vez con TDD: escribir primero los tests (uno por cada regla del docstring), verificar que fallan con `NotImplementedError` (RED), implementar, verificar que pasan (GREEN) y recién entonces commit.
- Verificar siempre con `python -m pytest` y, cuando aplique, recargando la página del servidor.
- Mantener la bitácora `ai-log.md` con los prompts clave, las decisiones aceptadas/rechazadas y cómo se comprobó cada paso.
