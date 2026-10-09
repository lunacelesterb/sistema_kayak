"""
Módulo de Interfaz Gráfica - Configuración de Importes de Cuotas
Permite consultar y actualizar los aranceles mensuales de Kayak, Natación y Ambas actividades.
Los cambios se guardan permanentemente en el archivo 'precios.json'.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datos import cargar_precios, guardar_precios


def abrir(root, callback_actualizar=None):
    """
    Abre una ventana secundaria para editar los importes mensuales de las cuotas.
    """
    ventana = tk.Toplevel(root)
    ventana.title("Configuración de Aranceles de Cuotas")
    ventana.geometry("380x280")
    ventana.resizable(False, False)
    ventana.grab_set()

    frame = ttk.Frame(ventana, padding=15)
    frame.pack(fill="both", expand=True)

    ttk.Label(
        frame,
        text="Modificación de Importes Mensuales ($)",
        font=("Segoe UI", 11, "bold"),
        foreground="#1b365d"
    ).grid(row=0, column=0, columnspan=2, pady=(0, 15))

    precios_actuales = cargar_precios()

    # Campo Kayak
    ttk.Label(frame, text="Cuota Kayak ($):").grid(row=1, column=0, padx=10, pady=8, sticky="e")
    entry_kayak = ttk.Entry(frame, width=15)
    entry_kayak.grid(row=1, column=1, padx=10, pady=8, sticky="w")
    entry_kayak.insert(0, str(precios_actuales.get("Kayak", 15000.0)))

    # Campo Natación
    ttk.Label(frame, text="Cuota Natación ($):").grid(row=2, column=0, padx=10, pady=8, sticky="e")
    entry_natacion = ttk.Entry(frame, width=15)
    entry_natacion.grid(row=2, column=1, padx=10, pady=8, sticky="w")
    entry_natacion.insert(0, str(precios_actuales.get("Natación", 18000.0)))

    # Campo Ambas Actividades
    ttk.Label(frame, text="Cuota Ambas (Combo) ($):").grid(row=3, column=0, padx=10, pady=8, sticky="e")
    entry_ambas = ttk.Entry(frame, width=15)
    entry_ambas.grid(row=3, column=1, padx=10, pady=8, sticky="w")
    entry_ambas.insert(0, str(precios_actuales.get("Ambas", 28000.0)))

    def guardar():
        try:
            val_kayak = float(entry_kayak.get().strip().replace(",", "."))
            val_natacion = float(entry_natacion.get().strip().replace(",", "."))
            val_ambas = float(entry_ambas.get().strip().replace(",", "."))

            if val_kayak <= 0 or val_natacion <= 0 or val_ambas <= 0:
                messagebox.showerror("Error", "Los importes deben ser mayores a cero.", parent=ventana)
                return

            nuevos = {
                "Kayak": val_kayak,
                "Natación": val_natacion,
                "Ambas": val_ambas
            }
            guardar_precios(nuevos)

            messagebox.showinfo(
                "Aranceles Actualizados",
                "Los nuevos importes fueron guardados exitosamente en 'precios.json'.\n"
                "Se aplicarán a los nuevos cobros.",
                parent=ventana
            )

            if callback_actualizar:
                callback_actualizar()

            ventana.destroy()

        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos.", parent=ventana)

    frame_botones = ttk.Frame(frame)
    frame_botones.grid(row=4, column=0, columnspan=2, pady=18)

    btn_guardar = ttk.Button(frame_botones, text="Guardar Cambios", command=guardar)
    btn_guardar.pack(side="left", padx=5)

    btn_cancelar = ttk.Button(frame_botones, text="Cancelar", command=ventana.destroy)
    btn_cancelar.pack(side="left", padx=5)

