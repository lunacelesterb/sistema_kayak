"""
Módulo de Interfaz Gráfica - Registro de Nuevos Socios
Permite ingresar los datos personales y deportivos de un alumno,
incluyendo actividades simples o combinadas (Ambas), turnos (Mañana/Tarde),
validaciones de campos y exigencia de apto médico.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from datos import Socio
from logica import cargar_socios, guardar_socios, buscar_socio


def abrir(root, callback_actualizar=None):
    """
    Abre una ventana secundaria (Toplevel) para dar de alta un nuevo socio.
    """
    ventana = tk.Toplevel(root)
    ventana.title("Alta de Socio - Sistema Náutico")
    ventana.geometry("440x430")
    ventana.resizable(False, False)
    ventana.grab_set()

    frame = ttk.Frame(ventana, padding=15)
    frame.pack(fill="both", expand=True)

    # 1. Campo DNI
    ttk.Label(frame, text="DNI (solo números):").grid(row=0, column=0, padx=8, pady=6, sticky="e")
    entry_dni = ttk.Entry(frame, width=22)
    entry_dni.grid(row=0, column=1, padx=8, pady=6, sticky="w")

    # 2. Campo Nombre
    ttk.Label(frame, text="Nombre:").grid(row=1, column=0, padx=8, pady=6, sticky="e")
    entry_nombre = ttk.Entry(frame, width=22)
    entry_nombre.grid(row=1, column=1, padx=8, pady=6, sticky="w")

    # 3. Campo Apellido
    ttk.Label(frame, text="Apellido:").grid(row=2, column=0, padx=8, pady=6, sticky="e")
    entry_apellido = ttk.Entry(frame, width=22)
    entry_apellido.grid(row=2, column=1, padx=8, pady=6, sticky="w")

    # 4. Campo Fecha de Nacimiento
    ttk.Label(frame, text="F. Nac. (DD/MM/AAAA):").grid(row=3, column=0, padx=8, pady=6, sticky="e")
    entry_fecha = ttk.Entry(frame, width=22)
    entry_fecha.grid(row=3, column=1, padx=8, pady=6, sticky="w")

    # 5. Selector de Actividad (Kayak, Natación, Ambas)
    ttk.Label(frame, text="Actividad:").grid(row=4, column=0, padx=8, pady=6, sticky="e")
    combo_clase = ttk.Combobox(
        frame,
        values=["Kayak", "Natación", "Ambas"],
        state="readonly",
        width=19
    )
    combo_clase.grid(row=4, column=1, padx=8, pady=6, sticky="w")
    combo_clase.set("Kayak")

    # 6. Selector de Turno (Mañana o Tarde)
    ttk.Label(frame, text="Turno:").grid(row=5, column=0, padx=8, pady=6, sticky="e")
    combo_turno = ttk.Combobox(
        frame,
        values=["Mañana", "Tarde"],
        state="readonly",
        width=19
    )
    combo_turno.grid(row=5, column=1, padx=8, pady=6, sticky="w")
    combo_turno.set("Mañana")

    # 7. Selector de Apto Médico
    lbl_apto = ttk.Label(frame, text="Apto Médico:")
    lbl_apto.grid(row=6, column=0, padx=8, pady=6, sticky="e")
    combo_apto = ttk.Combobox(
        frame,
        values=["No requiere"],
        state="readonly",
        width=19
    )
    combo_apto.grid(row=6, column=1, padx=8, pady=6, sticky="w")
    combo_apto.set("No requiere")

    # Evento interactivo para el Apto Médico según la actividad elegida
    def al_cambiar_actividad(event=None):
        actividad = combo_clase.get()
        if actividad in ("Natación", "Ambas"):
            combo_apto.config(values=["Sí (Entregado)", "No (Pendiente)"])
            combo_apto.set("No (Pendiente)")
        else:
            combo_apto.config(values=["No requiere"])
            combo_apto.set("No requiere")

    combo_clase.bind("<<ComboboxSelected>>", al_cambiar_actividad)

    # Función interna para guardar el socio
    def guardar():
        dni = entry_dni.get().strip()
        nombre = entry_nombre.get().strip()
        apellido = entry_apellido.get().strip()
        fecha = entry_fecha.get().strip()
        clase = combo_clase.get()
        turno = combo_turno.get()
        opcion_apto = combo_apto.get()

        # Validación 1: Campos vacíos
        if not dni or not nombre or not apellido or not fecha:
            messagebox.showwarning("Atención", "Por favor, complete todos los campos obligatorios.", parent=ventana)
            return

        # Validación 2: DNI numérico
        if not dni.isdigit() or len(dni) < 7 or len(dni) > 9:
            messagebox.showerror("Error", "El DNI debe contener únicamente entre 7 y 9 dígitos.", parent=ventana)
            return

        # Validación 3: Formato de fecha
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "La fecha de nacimiento debe tener el formato DD/MM/AAAA (ej: 20/04/2002).", parent=ventana)
            return

        socios = cargar_socios()

        # Validación 4: DNI único
        if buscar_socio(dni, socios) is not None:
            messagebox.showerror("Error", f"Ya existe un socio registrado con el DNI {dni}.", parent=ventana)
            return

        tiene_apto = True if "Sí" in opcion_apto else False

        nuevo_socio = Socio(
            dni=dni,
            nombre=nombre,
            apellido=apellido,
            fecha_de_nacimiento=fecha,
            clase=clase,
            turno=turno,
            apto_medico=tiene_apto
        )

        socios.append(nuevo_socio)
        guardar_socios(socios)

        mensaje_exito = f"Socio {nombre} {apellido} registrado con éxito.\nActividad: {clase} | Turno: {turno}."
        if clase in ("Natación", "Ambas") and not tiene_apto:
            mensaje_exito += "\n\n⚠️ Recordatorio: Solicitar certificado médico antes del ingreso al agua."

        messagebox.showinfo("Éxito", mensaje_exito, parent=ventana)

        if callback_actualizar:
            callback_actualizar()

        ventana.destroy()

    frame_botones = ttk.Frame(frame)
    frame_botones.grid(row=7, column=0, columnspan=2, pady=18)

    btn_guardar = ttk.Button(frame_botones, text="Guardar Socio", command=guardar)
    btn_guardar.pack(side="left", padx=5)

    btn_cancelar = ttk.Button(frame_botones, text="Cancelar", command=ventana.destroy)
    btn_cancelar.pack(side="left", padx=5)