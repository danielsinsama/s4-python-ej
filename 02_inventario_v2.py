# =====================================================================
# 02_inventario_v2.py  ·  Semana 4 · Curso de Python e IA (LAITEC)
# Inventario con menú, guardado en CSV y manejo de errores.
#
# ¿Necesito instalar algo o crear un entorno virtual (.venv)?
#   NO. "csv" viene dentro de Python (librería estándar).
#   Solo ejecuta en la terminal, dentro de la carpeta semana4:
#       python 02_inventario_v2.py      (Windows; o: py 02_inventario_v2.py)
#       python3 02_inventario_v2.py     (Mac)
# =====================================================================

import csv   # herramientas para leer/escribir CSV (viene con Python: sin pip ni venv)

# Orden de las columnas en el archivo inventario.csv
COLUMNAS = ["nombre", "precio", "stock", "categoria"]

# Menos de este número de unidades = "stock bajo"
STOCK_MINIMO = 5

# Datos de respaldo: se usan si inventario.csv todavía no existe
PRODUCTOS_EJEMPLO = [
    {"nombre": "Arroz", "precio": 4.5, "stock": 10, "categoria": "abarrotes"},
    {"nombre": "Leche", "precio": 3.8, "stock": 4, "categoria": "lacteos"},
    {"nombre": "Gaseosa 2L", "precio": 7.0, "stock": 2, "categoria": "bebidas"},
]


# ---------------------------------------------------------------------
# PASO 1 · Mostrar el inventario  (for + f-string)
# ---------------------------------------------------------------------
def mostrar_inventario(productos):
    print("\n--- INVENTARIO ---")
    for p in productos:                          # p = un producto (un diccionario)
        # f-string: lo que va entre { } se reemplaza por su valor
        # :.2f = mostrar el número con 2 decimales
        print(f"{p['nombre']:<12} S/ {p['precio']:.2f}   stock: {p['stock']}")


# ---------------------------------------------------------------------
# PASO 2 · Pedir un número sin que el programa se caiga  (try / except)
# ---------------------------------------------------------------------
def pedir_numero(mensaje):
    numero = -1                                  # empieza en -1 para que el while pregunte al menos 1 vez
    while numero < 0:                            # repite mientras no sea un número válido (>= 0)
        try:
            numero = float(input(mensaje))       # si escriben "abc", float() lanza ValueError
        except ValueError:
            print("Escribe un número, por ejemplo 4.50")
    return numero                                # aquí solo llega un número >= 0


# ---------------------------------------------------------------------
# PASO 3 · Agregar un producto  (input + append)
# ---------------------------------------------------------------------
def agregar_producto(productos):
    nombre = input("Nombre: ")
    precio = pedir_numero("Precio: ")            # antes era float(input(...)) y se caía con "abc"
    stock = int(pedir_numero("Stock: "))         # int() quita los decimales: 10.0 -> 10
    categoria = input("Categoría: ")
    productos.append({"nombre": nombre, "precio": precio,
                      "stock": stock, "categoria": categoria})
    guardar_inventario(productos)                # guardamos en el archivo apenas cambia algo
    print("Producto agregado y guardado.")


# ---------------------------------------------------------------------
# PASO 4 · Reporte: valor total, stock bajo y categorías  (acumulador + if + set)
# ---------------------------------------------------------------------
def reporte(productos):
    total = 0                                    # acumulador: empieza en 0 y va sumando
    categorias = set()                           # set() = conjunto vacío (no repite elementos)
    print("\nProductos con stock bajo:")
    for p in productos:
        total = total + p["precio"] * p["stock"] # valor de ese producto = precio x unidades
        categorias.add(p["categoria"])           # .add() agrega sin repetir
        if p["stock"] < STOCK_MINIMO:
            print(f"- {p['nombre']}: {p['stock']} unidades")
    print(f"Valor total del inventario: S/ {total:.2f}")
    print("Categorías:", categorias)


# ---------------------------------------------------------------------
# PASO 5 · Guardar la lista en un archivo  (with open + DictWriter)
# ---------------------------------------------------------------------
def guardar_inventario(productos):
    # "w" = escribir: crea el archivo o lo REEMPLAZA
    # newline="" evita filas en blanco extra en Windows
    # encoding="utf-8" guarda bien tildes y ñ
    # with ... as archivo: abre el archivo y lo cierra solo al terminar el bloque
    with open("inventario.csv", "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=COLUMNAS)
        escritor.writeheader()                   # 1ª fila: nombre,precio,stock,categoria
        escritor.writerows(productos)            # una fila por cada producto


# ---------------------------------------------------------------------
# PASO 6 · Leer el archivo  (with open + DictReader)
# ---------------------------------------------------------------------
def cargar_inventario():
    productos = []
    with open("inventario.csv", encoding="utf-8") as archivo:   # sin "w" = solo leer
        for fila in csv.DictReader(archivo):     # cada fila llega como diccionario
            fila["precio"] = float(fila["precio"])   # del archivo TODO llega como texto
            fila["stock"] = int(fila["stock"])
            productos.append(fila)
    return productos


# =====================================================================
# PROGRAMA PRINCIPAL
# =====================================================================
try:
    productos = cargar_inventario()              # falla si el archivo aún no existe
except FileNotFoundError:
    print("Aún no hay archivo. Empezamos con productos de ejemplo.")
    productos = PRODUCTOS_EJEMPLO

opcion = ""                                      # vacía para que el while entre la 1ª vez
while opcion != "4":
    print("\n1. Ver  2. Agregar  3. Reporte  4. Salir")
    opcion = input("Elige una opción: ")         # input() siempre devuelve texto: "1", no 1
    if opcion == "1":
        mostrar_inventario(productos)
    elif opcion == "2":
        agregar_producto(productos)
    elif opcion == "3":
        reporte(productos)
    elif opcion != "4":
        print("Opción no válida. Escribe 1, 2, 3 o 4.")
print("¡Hasta luego!")
