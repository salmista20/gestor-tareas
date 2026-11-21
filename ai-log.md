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
