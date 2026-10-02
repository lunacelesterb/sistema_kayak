import tkinter as tk
from tkinter import filedialog, messagebox

from datos import cargar_clientes, exportar_clientes, guardar_clientes
from pantalla_clientes import abrir_pantalla_clientes
from pantalla_estadisticas import abrir_pantalla_estadisticas
from pantalla_renovacion import abrir_pantalla_renovacion

clientes = cargar_clientes()


def exportar_datos():
    """Permite seleccionar dónde guardar una copia JSON."""
    nombre_archivo = filedialog.asksaveasfilename(
        title="Exportar clientes",
        defaultextension=".json",
        filetypes=[("Archivo JSON", "*.json")],
    )

    if nombre_archivo == "":
        return

    exportar_clientes(clientes, nombre_archivo)
    messagebox.showinfo(
        "Exportación exitosa", "Los datos fueron exportados correctamente."
    )


def salir():
    """Guarda los datos y cierra el programa."""
    guardar_clientes(clientes)
    ventana.destroy()


ventana = tk.Tk()
ventana.title("AquaGestión")
ventana.geometry("500x500")
ventana.resizable(False, False)

tk.Label(
    ventana, text="AquaGestión", font=("Arial", 26, "bold"), fg="darkblue"
).pack(pady=20)

tk.Label(
    ventana, text="Escuela de kayak y natación", font=("Arial", 12)
).pack(pady=5)

tk.Button(
    ventana,
    text="Registrar cliente",
    width=30,
    command=lambda: abrir_pantalla_clientes(
        ventana, clientes, guardar_clientes
    ),
).pack(pady=10)

tk.Button(
    ventana,
    text="Renovar seguro",
    width=30,
    command=lambda: abrir_pantalla_renovacion(
        ventana, clientes, guardar_clientes
    ),
).pack(pady=10)

tk.Button(
    ventana,
    text="Ver estadísticas",
    width=30,
    command=lambda: abrir_pantalla_estadisticas(ventana, clientes),
).pack(pady=10)

tk.Button(
    ventana, text="Exportar datos a JSON", width=30, command=exportar_datos
).pack(pady=10)

tk.Button(ventana, text="Salir", width=30, command=salir).pack(pady=10)

ventana.mainloop()