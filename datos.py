import json
import os

ARCHIVO_JSON = "clientes.json"


def cargar_clientes():
    """Carga los clientes almacenados en clientes.json."""
    if not os.path.exists(ARCHIVO_JSON):
        return []

    try:
        with open(ARCHIVO_JSON, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except json.JSONDecodeError:
        return []


def guardar_clientes(clientes):
    """Guarda la lista de clientes en el archivo JSON."""
    with open(ARCHIVO_JSON, "w", encoding="utf-8") as archivo:
        json.dump(clientes, archivo, indent=4, ensure_ascii=False)


def exportar_clientes(clientes, nombre_archivo):
    """Permite exportar los clientes a otro archivo JSON."""
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        json.dump(clientes, archivo, indent=4, ensure_ascii=False)