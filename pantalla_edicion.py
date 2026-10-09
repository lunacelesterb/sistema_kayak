"""
Módulo de Interfaz Gráfica - Modificación de Alumnos / Socios
Permite editar los datos de un socio existente: nombre, apellido, fecha de nacimiento,
actividad (Kayak, Natación, Ambas), turno (Mañana/Tarde), apto médico y estado.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from logica import actualizar_socio, buscar_socio


def abrir(root, socio, callback_actualizar=None):
    """
    Abre una ventana modal para editar los datos del alumno seleccionado.
    """
    if not socio:
        messagebox.showwarning("Atención", "No se especificó ningún alumno para modificar.")
        return

    ventana = tk.Toplevel(root)
    ventana.title(f"Modificar Alumno - DNI: {socio.dni}")
    ventana.geometry("450x470")
    ventana.resizable(False, False)
    ventana.grab_set()

    frame = ttk.Frame(ventana, padding=15)
    frame.pack(fill="both", expand=True)

    ttk.Label(
        frame,
        text=f"Modificando datos de: {socio.nombre} {socio.apellido}",
        font=("Segoe UI", 11, "bold"),
        foreground="#1b365d"
    ).grid(row=0, column=0, columnspan=2, pady=(0, 15))

    # 1. DNI (Identificador único, protegido contra cambios accidentales)
    ttk.Label(frame, text="DNI:").grid(row=1, column=0, padx=8, pady=6, sticky="e")
    entry_dni = ttk.Entry(frame, width=22)
    entry_dni.grid(row=1, column=1, padx=8, pady=6, sticky="w")
    entry_dni.insert(0, str(socio.dni))
    entry_dni.config(state="disabled")

    # 2. Nombre
    ttk.Label(frame, text="Nombre:").grid(row=2, column=0, padx=8, pady=6, sticky="e")
    entry_nombre = ttk.Entry(frame, width=22)
    entry_nombre.grid(row=2, column=1, padx=8, pady=6, sticky="w")
    entry_nombre.insert(0, socio.nombre)

    # 3. Apellido
    ttk.Label(frame, text="Apellido:").grid(row=3, column=0, padx=8, pady=6, sticky="e")
    entry_apellido = ttk.Entry(frame, width=22)
    entry_apellido.grid(row=3, column=1, padx=8, pady=6, sticky="w")
    entry_apellido.insert(0, socio.apellido)

    # 4. Fecha de Nacimiento
    ttk.Label(frame, text="F. Nac. (DD/MM/AAAA):").grid(row=4, column=0, padx=8, pady=6, sticky="e")
    entry_fecha = ttk.Entry(frame, width=22)
    entry_fecha.grid(row=4, column=1, padx=8, pady=6, sticky="w")
    entry_fecha.insert(0, str(socio.nacimiento))

    # 5. Actividad
    ttk.Label(frame, text="Actividad:").grid(row=5, column=0, padx=8, pady=6, sticky="e")
    combo_clase = ttk.Combobox(
        frame,
        values=["Kayak", "Natación", "Ambas"],
        state="readonly",
        width=19
    )
    combo_clase.grid(row=5, column=1, padx=8, pady=6, sticky="w")
    combo_clase.set(socio.clase if socio.clase in ("Kayak", "Natación", "Ambas") else "Kayak")

    # 6. Turno
    ttk.Label(frame, text="Turno:").grid(row=6, column=0, padx=8, pady=6, sticky="e")
    combo_turno = ttk.Combobox(
        frame,
        values=["Mañana", "Tarde"],
        state="readonly",
        width=19
    )
    combo_turno.grid(row=6, column=1, padx=8, pady=6, sticky="w")
    combo_turno.set(socio.turno if socio.turno in ("Mañana", "Tarde") else "Mañana")

    # 7. Apto Médico
    ttk.Label(frame, text="Apto Médico:").grid(row=7, column=0, padx=8, pady=6, sticky="e")
    combo_apto = ttk.Combobox(
        frame,
        values=["Sí (Entregado)", "No (Pendiente)", "No requiere"],
        state="readonly",
        width=19
    )
    combo_apto.grid(row=7, column=1, padx=8, pady=6, sticky="w")

    if combo_clase.get() == "Kayak":
        combo_apto.set("No requiere")
    else:
        combo_apto.set("Sí (Entregado)" if socio.apto_medico else "No (Pendiente)")

    def al_cambiar_actividad(event=None):
        actividad = combo_clase.get()
        if actividad in ("Natación", "Ambas"):
            combo_apto.config(values=["Sí (Entregado)", "No (Pendiente)"])
            combo_apto.set("Sí (Entregado)" if socio.apto_medico else "No (Pendiente)")
        else:
            combo_apto.config(values=["No requiere"])
            combo_apto.set("No requiere")

    combo_clase.bind("<<ComboboxSelected>>", al_cambiar_actividad)

    # 8. Estado del Socio (Activo o Inactivo)
    ttk.Label(frame, text="Estado:").grid(row=8, column=0, padx=8, pady=6, sticky="e")
    combo_estado = ttk.Combobox(
        frame,
        values=["Activo", "Inactivo"],
        state="readonly",
        width=19
    )
    combo_estado.grid(row=8, column=1, padx=8, pady=6, sticky="w")
    combo_estado.set(socio.estado if socio.estado in ("Activo", "Inactivo") else "Activo")

    def guardar():
        nombre = entry_nombre.get().strip()
        apellido = entry_apellido.get().strip()
        fecha = entry_fecha.get().strip()
        clase = combo_clase.get()
        turno = combo_turno.get()
        opcion_apto = combo_apto.get()
        estado = combo_estado.get()

        if not nombre or not apellido or not fecha:
            messagebox.showwarning("Atención", "Complete todos los campos de texto.", parent=ventana)
            return

        try:
            datetime.strptime(fecha, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "La fecha debe tener el formato DD/MM/AAAA.", parent=ventana)
            return

        tiene_apto = True if "Sí" in opcion_apto else False

        datos_nuevos = {
            "nombre": nombre,
            "apellido": apellido,
            "nacimiento": fecha,
            "clase": clase,
            "turno": turno,
            "apto_medico": tiene_apto,
            "estado": estado
        }

        exito = actualizar_socio(socio.dni, datos_nuevos)
        if exito:
            messagebox.showinfo(
                "Modificación Exitosa",
                f"Los datos de {nombre} {apellido} fueron actualizados correctamente.",
                parent=ventana
            )
            if callback_actualizar:
                callback_actualizar()
            ventana.destroy()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el registro.", parent=ventana)

    frame_botones = ttk.Frame(frame)
    frame_botones.grid(row=9, column=0, columnspan=2, pady=18)

    btn_guardar = ttk.Button(frame_botones, text="Guardar Cambios", command=guardar)
    btn_guardar.pack(side="left", padx=5)

    btn_cancelar = ttk.Button(frame_botones, text="Cancelar", command=ventana.destroy)
    btn_cancelar.pack(side="left", padx=5)

