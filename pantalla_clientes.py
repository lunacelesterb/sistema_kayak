import tkinter as tk
from tkinter import ttk, messagebox
from datos import Socio
from logica import cargar_socios, guardar_socios

def abrir(root):
    ventana = tk.Toplevel(root)
    ventana.title("Registro de Socio")
    ventana.geometry("400x350")

    ttk.Label(ventana, text="DNI:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_dni = ttk.Entry(ventana)
    entry_dni.grid(row=0, column=1, padx=10, pady=5)

    ttk.Label(ventana, text="Nombre:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_nombre = ttk.Entry(ventana)
    entry_nombre.grid(row=1, column=1, padx=10, pady=5)

    ttk.Label(ventana, text="Apellido:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_apellido = ttk.Entry(ventana)
    entry_apellido.grid(row=2, column=1, padx=10, pady=5)

    ttk.Label(ventana, text="Fecha Nac. (DD/MM/AAAA):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entry_fecha = ttk.Entry(ventana)
    entry_fecha.grid(row=3, column=1, padx=10, pady=5)

    ttk.Label(ventana, text="Clase:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    combo_clase = ttk.Combobox(ventana, values=["Kayak", "Natación"], state="readonly")
    combo_clase.grid(row=4, column=1, padx=10, pady=5)
    combo_clase.set("Kayak")

    ttk.Label(ventana, text="¿Apto Médico? (Natación):").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    combo_apto = ttk.Combobox(ventana, values=["No", "Sí"], state="readonly")
    combo_apto.grid(row=5, column=1, padx=10, pady=5)
    combo_apto.set("No")

    def guardar():
        dni = entry_dni.get()
        nombre = entry_nombre.get()
        apellido = entry_apellido.get()
        fecha = entry_fecha.get()
        clase = combo_clase.get()
        apto = True if combo_apto.get() == "Sí" else False

        if not dni or not nombre or not apellido or not fecha:
            messagebox.showwarning("Error", "Completá los datos básicos")
            return

        socios = cargar_socios()
        
        for s in socios:
            if s.dni == dni:
                messagebox.showerror("Error", "El DNI ya existe")
                return

        # Acá mandamos los datos en el orden exacto del __init__
        nuevo_socio = Socio(dni, nombre, apellido, fecha, clase, apto)
        socios.append(nuevo_socio)
        guardar_socios(socios)
        messagebox.showinfo("Éxito", "Socio guardado correctamente")
        ventana.destroy()

    ttk.Button(ventana, text="Guardar Socio", command=guardar).grid(row=6, column=0, columnspan=2, pady=15)