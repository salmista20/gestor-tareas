"""Vista web del gestor de tareas, solo en tu computadora.

Uso: python servidor.py [puerto]
Abre http://127.0.0.1:8000 en el navegador. Ctrl+C para detener.

Este archivo viene listo: no necesitas modificarlo. En cada petición vuelve
a cargar tareas.py, así que tus cambios se ven al recargar la página, sin
reiniciar el servidor.
"""

import html
import importlib
import sys
import threading
import traceback
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlsplit

import almacen

HOST = "127.0.0.1"
PUERTO = 8000

TAREAS_DE_EJEMPLO = [
    {"id": 1, "titulo": "Instalar OpenCode", "hecha": True},
    {"id": 2, "titulo": "Leer el README", "hecha": False},
    {"id": 3, "titulo": "Escribir el primer test", "hecha": False},
]

# Ruta del formulario -> (función de tareas.py, palabra del aviso de éxito)
ACCIONES = {
    "/agregar": ("agregar", "agregada"),
    "/completar": ("completar", "completada"),
    "/eliminar": ("eliminar", "eliminada"),
    "/editar": ("editar", "editada"),
}

# Aviso que se muestra una sola vez en la siguiente carga de la página:
# una tupla (tipo, texto), donde tipo es "exito", "pendiente" o "error".
aviso = None
# El navegador puede abrir varias conexiones; se atiende una petición a la vez.
candado = threading.Lock()

ESTILOS = """
body { margin: 0; background: #F3F6FA; color: #1F2933;
       font-family: "Segoe UI", Arial, sans-serif; font-size: 22px; }
main { max-width: 920px; margin: 0 auto; padding: 32px 24px; }
h1 { margin: 0; color: #1F4E79; font-size: 44px; }
.contador { margin: 6px 0 24px; color: #52606D; }
.aviso { margin: 0 0 16px; padding: 14px 18px; border-radius: 8px;
         border-left: 8px solid; }
.exito { background: #E3F4E1; border-color: #2E7D32; color: #1B5E20; }
.pendiente { background: #FFF4D6; border-color: #C98A00; color: #6B4A00; }
.error { background: #FDE2E2; border-color: #C62828; color: #8E1B1B; }
form { margin: 0; display: flex; gap: 10px; }
.nueva { margin-bottom: 24px; }
input { flex: 1; min-width: 0; font: inherit; padding: 10px 14px;
        border: 2px solid #C5D3E2; border-radius: 8px; }
button, summary { font: inherit; font-size: 18px; padding: 10px 16px;
                  border: 2px solid #1F4E79; border-radius: 8px;
                  background: #1F4E79; color: #FFFFFF; cursor: pointer; }
button:hover, summary:hover { filter: brightness(1.15); }
ul { list-style: none; margin: 0; padding: 0; }
.tarea { display: flex; flex-wrap: wrap; align-items: center; gap: 12px;
         margin-bottom: 12px; padding: 14px 18px; background: #FFFFFF;
         border-radius: 10px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12); }
.id { min-width: 2.5em; color: #7B8794; }
.titulo { flex: 1; min-width: 220px; }
.hecha .titulo { color: #2E7D32; text-decoration: line-through; }
.botones { display: flex; flex-wrap: wrap; align-items: flex-start; gap: 8px; }
summary { list-style: none; background: #FFFFFF; color: #1F4E79; }
summary::-webkit-details-marker { display: none; }
details[open] form { margin-top: 8px; }
.eliminar { background: #FFFFFF; color: #C62828; border-color: #C62828; }
.vacia { padding: 14px 0; color: #52606D; }
.pie { margin-top: 32px; font-size: 16px; color: #7B8794; }
"""


def cargar_modulo_tareas():
    """Vuelve a importar tareas.py para usar su última versión.

    Devuelve (modulo, None), o (None, "Tipo: mensaje") si tareas.py tiene
    un error, por ejemplo mientras el agente lo está editando.
    """
    try:
        if "tareas" in sys.modules:
            return importlib.reload(sys.modules["tareas"]), None
        return importlib.import_module("tareas"), None
    except Exception as error:
        return None, f"{type(error).__name__}: {error}"


def leer_tareas():
    """Devuelve (lista, None), o ([], mensaje) si tareas.json no se puede leer."""
    try:
        return almacen.cargar(), None
    except (OSError, ValueError) as error:
        return [], f"No se pudo leer {almacen.RUTA.name}: {error}"


def leer_argumentos(nombre, campos):
    """Arma los argumentos de la función a partir de los campos del formulario."""
    argumentos = []
    if nombre != "agregar":
        texto = campos.get("id", "")
        try:
            argumentos.append(int(texto))
        except ValueError:
            raise ValueError(f"El id debe ser un número entero, no '{texto}'") from None
    if nombre in ("agregar", "editar"):
        argumentos.append(campos.get("titulo", ""))
    return argumentos


def ejecutar(nombre, participio, campos):
    """Llama a la función de tareas.py que pidió el formulario.

    Guarda la lista solo si la función terminó sin errores.
    Devuelve el aviso para la página: (tipo, texto).
    """
    modulo, error = cargar_modulo_tareas()
    if error:
        return "error", f"tareas.py tiene un error: {error}"
    lista, error = leer_tareas()
    if error:
        return "error", error

    try:
        argumentos = leer_argumentos(nombre, campos)
        resultado = getattr(modulo, nombre)(lista, *argumentos)
    except NotImplementedError as error:
        mensaje = str(error) or f"{nombre}() aún no está implementada"
        return "pendiente", f"{mensaje}. Escribe primero su test y luego impleméntala en tareas.py."
    except ValueError as error:
        return "error", str(error)
    except Exception as error:
        traceback.print_exc()
        return "error", f"Error inesperado en tareas.py: {type(error).__name__}: {error}"

    almacen.guardar(lista)
    if not isinstance(resultado, dict) or "id" not in resultado:
        return "pendiente", f"Se guardó el cambio, pero {nombre}() no devolvió la tarea. Revisa su return."
    return "exito", f"Tarea {resultado['id']} {participio}"


def contar(cantidad, singular, plural):
    """Devuelve, por ejemplo, "1 tarea" o "3 tareas"."""
    return f"{cantidad} {singular if cantidad == 1 else plural}"


def construir_fila(tarea):
    """Arma el HTML de una tarea con sus botones."""
    id_tarea = html.escape(str(tarea.get("id", "")))
    titulo = html.escape(str(tarea.get("titulo", "")))
    clase = "tarea hecha" if tarea.get("hecha") else "tarea"
    oculto = f'<input type="hidden" name="id" value="{id_tarea}">'
    return f"""
<li class="{clase}">
  <span class="id">#{id_tarea}</span>
  <span class="titulo">{titulo}</span>
  <span class="botones">
    <form method="post" action="/completar">{oculto}<button>Completar</button></form>
    <details>
      <summary>Editar</summary>
      <form method="post" action="/editar">{oculto}<input name="titulo" value="{titulo}"><button>Guardar</button></form>
    </details>
    <form method="post" action="/eliminar">{oculto}<button class="eliminar">Eliminar</button></form>
  </span>
</li>"""


def construir_pagina(lista, avisos):
    """Arma el HTML completo de la página."""
    hechas = sum(1 for tarea in lista if tarea.get("hecha"))
    contador = " · ".join([
        contar(len(lista), "tarea", "tareas"),
        contar(hechas, "hecha", "hechas"),
        contar(len(lista) - hechas, "pendiente", "pendientes"),
    ])
    bloques = "".join(
        f'<p class="aviso {tipo}">{html.escape(texto)}</p>' for tipo, texto in avisos
    )
    filas = "".join(construir_fila(tarea) for tarea in lista)
    if not filas:
        filas = '<li class="vacia">No hay tareas. Agrega la primera con el formulario de arriba.</li>'
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Gestor de tareas</title>
<style>{ESTILOS}</style>
</head>
<body>
<main>
<h1>Gestor de tareas</h1>
<p class="contador">{contador}</p>
{bloques}
<form class="nueva" method="post" action="/agregar">
  <input name="titulo" placeholder="Nueva tarea" autofocus>
  <button>Agregar</button>
</form>
<ul>{filas}</ul>
<p class="pie">Esta página vuelve a cargar tareas.py cada vez que la recargas (F5).</p>
</main>
</body>
</html>"""


class Manejador(BaseHTTPRequestHandler):
    """Atiende las peticiones del navegador."""

    def do_GET(self):
        global aviso
        if urlsplit(self.path).path != "/":
            self.send_error(404)
            return
        with candado:
            avisos = []
            _, error = cargar_modulo_tareas()
            if error:
                avisos.append(("error", f"tareas.py tiene un error: {error}"))
            if aviso and aviso not in avisos:
                avisos.append(aviso)
            aviso = None
            lista, error = leer_tareas()
            if error:
                avisos.append(("error", error))
            datos = construir_pagina(lista, avisos).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(datos)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(datos)

    def do_POST(self):
        global aviso
        accion = ACCIONES.get(urlsplit(self.path).path)
        if accion is None:
            self.send_error(404)
            return
        largo = int(self.headers.get("Content-Length") or 0)
        cuerpo = self.rfile.read(largo).decode("utf-8", errors="replace")
        campos = {
            clave: valores[0]
            for clave, valores in parse_qs(cuerpo, keep_blank_values=True).items()
        }
        with candado:
            aviso = ejecutar(*accion, campos)
        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()

    def log_message(self, formato, *argumentos):
        """No muestra cada petición en la consola, para que se lean los errores."""


class Servidor(ThreadingHTTPServer):
    """Servidor web local que avisa si el puerto ya está ocupado."""

    # En Windows, reutilizar la dirección dejaría abrir dos servidores en el
    # mismo puerto sin ningún error; así el segundo falla con un mensaje claro.
    allow_reuse_address = sys.platform != "win32"


def main():
    puerto = PUERTO
    if len(sys.argv) > 1:
        if not sys.argv[1].isdigit():
            print("El puerto debe ser un número. Ejemplo: python servidor.py 8001")
            return 1
        puerto = int(sys.argv[1])

    try:
        servidor = Servidor((HOST, puerto), Manejador)
    except (OSError, OverflowError):
        print(f"No se pudo usar el puerto {puerto}: puede que otro programa lo esté usando.")
        print(f"Prueba con otro puerto: python servidor.py {puerto + 1}")
        return 1

    if not almacen.RUTA.exists():
        almacen.guardar(TAREAS_DE_EJEMPLO)
        print(f"Se creó {almacen.RUTA.name} con tres tareas de ejemplo.")

    url = f"http://{HOST}:{puerto}"
    print(f"Gestor de tareas en {url}")
    print("Ctrl+C para detener")
    webbrowser.open(url)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        servidor.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
