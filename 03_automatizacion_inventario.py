# =====================================================================
# 03_automatizacion_inventario.py  ·  Semana 4 · Curso de Python e IA (LAITEC)
# Lee los CSV de todas las sedes y arma un consolidado en reportes/.
# (Correo automático y tarea programada: Semana 6 · APIs)
#
# ¿Necesito instalar algo o crear un entorno virtual (.venv)?
#   NO. csv y pathlib vienen dentro de Python
#   (librería estándar). No hace falta pip ni .venv.
#
# Cómo ejecutarlo (terminal abierta en la carpeta semana4):
#       python 03_automatizacion_inventario.py      (Windows; o: py ...)
#       python3 03_automatizacion_inventario.py     (Mac)
#
# Carpeta esperada:
#   semana4/
#   ├── 03_automatizacion_inventario.py
#   ├── sedes/        <- chiclayo.csv, lambayeque.csv, ferrenafe.csv
#   └── reportes/     <- la crea el script
# =====================================================================

import csv                                 # leer/escribir CSV
from pathlib import Path                   # rutas y carpetas que funcionan en Windows y Mac

# ---------------------------------------------------------------------
# CONFIGURACIÓN (lo único que cambias para usarlo en tu caso)
# ---------------------------------------------------------------------
CARPETA_SEDES = Path("sedes")              # de aquí se leen los CSV
CARPETA_REPORTES = Path("reportes")        # aquí se guarda el consolidado
COLUMNAS = ["sede", "nombre", "precio", "stock", "categoria"]


# ---------------------------------------------------------------------
# PASO 1 · Leer UNA sede (un archivo CSV)
# ---------------------------------------------------------------------
def leer_sede(ruta):
    productos = []
    with open(ruta, encoding="utf-8") as archivo:
        for fila in csv.DictReader(archivo):           # cada fila = un diccionario
            try:                                       # un try POR FILA: si una falla, seguimos
                fila["precio"] = float(fila["precio"]) # "4.5" -> 4.5
                fila["stock"] = int(fila["stock"])     # "diez" -> ValueError
            except ValueError:
                print("  Fila ignorada en", ruta.name, "->", fila["nombre"])
                continue                               # salta a la siguiente fila
            fila["sede"] = ruta.stem                   # .stem = nombre sin .csv -> "chiclayo"
            productos.append(fila)
    return productos


# ---------------------------------------------------------------------
# PASO 2 · Leer TODAS las sedes y juntarlas (lote)
# ---------------------------------------------------------------------
def consolidar():
    todos = []
    for ruta in CARPETA_SEDES.glob("*.csv"):           # * = cualquier nombre que termine en .csv
        print("Leyendo", ruta.name)                    # .name = "chiclayo.csv"
        for producto in leer_sede(ruta):
            todos.append(producto)
    return todos


# ---------------------------------------------------------------------
# PASO 3 · Guardar el consolidado en un CSV
# ---------------------------------------------------------------------
def guardar_csv(productos, ruta):
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
        escritor.writeheader()                         # 1ª fila: títulos de columnas
        escritor.writerows(productos)                  # una fila por producto
    print("Consolidado guardado en", ruta)


# =====================================================================
# PROGRAMA PRINCIPAL · llama a las funciones en orden
# =====================================================================
productos = consolidar()                               # 1. leer y juntar las sedes

if len(productos) == 0:                                # ¿no encontró ningún CSV?
    print("No se encontraron archivos en la carpeta 'sedes'.")
else:
    CARPETA_REPORTES.mkdir(exist_ok=True)              # 2. crea reportes/ (si ya existe, no pasa nada)
    guardar_csv(productos, CARPETA_REPORTES / "consolidado.csv")   # "/" une carpeta + archivo
    print("Listo:", len(productos), "productos consolidados de todas las sedes.")
