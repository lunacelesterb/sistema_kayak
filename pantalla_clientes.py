"""
================================================================================
ARCHIVO: pantalla_clientes.py (Formulario de Alta de Nuevos Alumnos / Socios)
================================================================================

1. PROPÓSITO GENERAL:
   Este módulo abre una ventana emergente para inscribir a un nuevo alumno en la
   escuela náutica. Su objetivo práctico es pedir los datos personales y deportivos,
   validar que no haya errores de carga (como un DNI con letras, un DNI duplicado o
   una fecha inexistente) y guardar al nuevo socio en el archivo 'clientes.json'.

2. ELEMENTOS VISUALES / INTERFAZ:
   - Ventana Secundaria ('ventana = tk.Toplevel'): Mide 480x500 píxeles, tiene tamaño
     fijo para conservar la estética del formulario y fondo difuminado ('fondo.jpg').
   - Botón Conmutador de Tema (🌙 / ☀️): Arriba a la derecha para cambiar entre Día y Noche.
   - Tarjeta de Formulario ('frame = ttk.LabelFrame'): Cuadro con título en Azul Glicina
     (#779be7) que organiza los campos en una cuadrícula ('grid') de 8 filas y 2 columnas:
     * 4 Cajas de texto ('ttk.Entry' de ancho 22): DNI, Nombre, Apellido y Fecha de Nacimiento.
     * 3 Listas desplegables ('ttk.Combobox' de ancho 19 en modo 'readonly'):
       Actividad (Kayak / Natación / Ambas), Turno (Mañana / Tarde) y Apto Médico.
   - Botones de Acción ('btn_guardar' y 'btn_cancelar'): Con efecto Hover en color
     Cielo Fresco (#49b6ff) y aumento de tamaño de fuente al hacer clic.

3. EXPLICACIÓN LÍNEA POR LÍNEA:
   Cada instrucción está comentada debajo explicando qué controla y cómo responde
   ante las acciones del usuario.
================================================================================
"""

# Aquí importamos 'tkinter' y sus submódulos 'ttk' (controles estilizados) y 'messagebox' (alertas)
import tkinter as tk
from tkinter import ttk, messagebox
# Aquí importamos 'datetime' para comprobar que la fecha de nacimiento escrita exista en el calendario
from datetime import datetime
# Aquí importamos el molde 'Socio' desde nuestro archivo 'datos.py'
from datos import Socio
# Aquí importamos las funciones de lectura/escritura JSON y el motor visual desde 'logica.py'
from logica import (
    cargar_socios,
    guardar_socios,
    configurar_estilos_modernos,
    crear_boton_tema
)


def abrir(root, callback_actualizar=None):
    """
    Función que construye y abre la ventana emergente para registrar un nuevo alumno.
    Recibe 'root' (la ventana principal) y 'callback_actualizar' (para refrescar el inicio al guardar).
    """
    # Aquí se crea una ventana secundaria ('Toplevel') dependiente de la ventana principal
    ventana = tk.Toplevel(root)
    # Aquí se define el título de la ventana
    ventana.title("Alta de Socio - Sistema Náutico")
    # Aquí se define el tamaño de la ventana: 480 píxeles de ancho por 500 píxeles de alto
    ventana.geometry("480x500")
    # Aquí bloqueamos el cambio de tamaño manual (ancho=False, alto=False) para que no se desarme la grilla
    ventana.resizable(False, False)
    # 'grab_set()' hace que la ventana sea "modal": obliga a terminar o cancelar aquí antes de tocar la ventana de atrás
    ventana.grab_set()

    # Aquí aplicamos la imagen de fondo difuminada, los colores azules y los efectos en los botones
    configurar_estilos_modernos(ventana)
    # Aquí agregamos el botón 🌙 / ☀️ arriba a la derecha para cambiar entre Modo Día y Modo Noche
    crear_boton_tema(ventana, padx=18, pady=(10, 2))

    # Aquí se crea la tarjeta principal ('LabelFrame') que contiene todo el formulario
    frame = ttk.LabelFrame(ventana, text=" ✨ Datos del Nuevo Alumno / Socio ", padding=15)
    frame.pack(fill="both", expand=True, padx=18, pady=(4, 16))

    # --- FILA 0: Campo DNI ---
    # Etiqueta de texto ubicada en la fila 0, columna 0, alineada a la derecha (sticky="e" de East/Este)
    ttk.Label(frame, text="DNI (solo números):", style="Card.TLabel").grid(row=0, column=0, padx=8, pady=6, sticky="e")
    # Caja de entrada de texto de 22 caracteres de ancho ubicada en la fila 0, columna 1 (sticky="w" de West/Oeste)
    entry_dni = ttk.Entry(frame, width=22)
    entry_dni.grid(row=0, column=1, padx=8, pady=6, sticky="w")

    # --- FILA 1: Campo Nombre ---
    ttk.Label(frame, text="Nombre:", style="Card.TLabel").grid(row=1, column=0, padx=8, pady=6, sticky="e")
    entry_nombre = ttk.Entry(frame, width=22)
    entry_nombre.grid(row=1, column=1, padx=8, pady=6, sticky="w")

    # --- FILA 2: Campo Apellido ---
    ttk.Label(frame, text="Apellido:", style="Card.TLabel").grid(row=2, column=0, padx=8, pady=6, sticky="e")
    entry_apellido = ttk.Entry(frame, width=22)
    entry_apellido.grid(row=2, column=1, padx=8, pady=6, sticky="w")

    # --- FILA 3: Campo Fecha de Nacimiento ---
    ttk.Label(frame, text="F. Nac. (DD/MM/AAAA):", style="Card.TLabel").grid(row=3, column=0, padx=8, pady=6, sticky="e")
    entry_fecha = ttk.Entry(frame, width=22)
    entry_fecha.grid(row=3, column=1, padx=8, pady=6, sticky="w")

    # --- FILA 4: Lista Desplegable de Actividad ---
    ttk.Label(frame, text="Actividad:", style="Card.TLabel").grid(row=4, column=0, padx=8, pady=6, sticky="e")
    # 'state="readonly"' impide que el usuario escriba a mano otra actividad que no esté en la lista
    combo_clase = ttk.Combobox(
        frame,
        values=["Kayak", "Natación", "Ambas"],
        state="readonly",
        width=19
    )
    combo_clase.grid(row=4, column=1, padx=8, pady=6, sticky="w")
    # Dejamos preseleccionada la opción "Kayak" por defecto
    combo_clase.set("Kayak")

    # --- FILA 5: Lista Desplegable de Turno ---
    ttk.Label(frame, text="Turno:", style="Card.TLabel").grid(row=5, column=0, padx=8, pady=6, sticky="e")
    combo_turno = ttk.Combobox(
        frame,
        values=["Mañana", "Tarde"],
        state="readonly",
        width=19
    )
    combo_turno.grid(row=5, column=1, padx=8, pady=6, sticky="w")
    combo_turno.set("Mañana")

    # --- FILA 6: Lista Desplegable de Apto Médico ---
    lbl_apto = ttk.Label(frame, text="Apto Médico:", style="Card.TLabel")
    lbl_apto.grid(row=6, column=0, padx=8, pady=6, sticky="e")
    combo_apto = ttk.Combobox(
        frame,
        values=["No requiere"],
        state="readonly",
        width=19
    )
    combo_apto.grid(row=6, column=1, padx=8, pady=6, sticky="w")
    combo_apto.set("No requiere")

    # Aquí se maneja lo que pasa cuando el usuario cambia la Actividad en el desplegable:
    def al_cambiar_actividad(event=None):
        actividad = combo_clase.get()
        # Si elige "Natación" o "Ambas", el apto médico es obligatorio, por lo que habilitamos "Sí" o "No"
        if actividad in ("Natación", "Ambas"):
            combo_apto.config(values=["Sí (Entregado)", "No (Pendiente)"])
            combo_apto.set("No (Pendiente)")
        else:
            # Si elige solo "Kayak", no se exige certificado médico
            combo_apto.config(values=["No requiere"])
            combo_apto.set("No requiere")

    # Conectamos el evento '<<ComboboxSelected>>' para que al elegir una actividad se ejecute 'al_cambiar_actividad'
    combo_clase.bind("<<ComboboxSelected>>", al_cambiar_actividad)

    # Aquí se maneja lo que pasa cuando el usuario hace clic en el botón "💾 Guardar Socio":
    def guardar():
        # 1. Leemos el texto que el usuario escribió en cada campo y quitamos espacios vacíos (.strip())
        dni = entry_dni.get().strip()
        nombre = entry_nombre.get().strip()
        apellido = entry_apellido.get().strip()
        fecha = entry_fecha.get().strip()
        clase = combo_clase.get()
        turno = combo_turno.get()
        opcion_apto = combo_apto.get()

        # Validación 1: Verificar que no haya dejado ningún campo de texto en blanco
        if not dni or not nombre or not apellido or not fecha:
            messagebox.showwarning("Atención", "Por favor, complete todos los campos obligatorios.", parent=ventana)
            return

        # Validación 2: Verificar que el DNI tenga solo números (.isdigit()) y entre 7 y 9 dígitos
        if not dni.isdigit() or len(dni) < 7 or len(dni) > 9:
            messagebox.showerror("Error", "El DNI debe contener únicamente entre 7 y 9 dígitos.", parent=ventana)
            return

        # Validación 3: Verificar que la fecha tenga formato real DD/MM/AAAA (día/mes/año)
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "La fecha de nacimiento debe tener el formato DD/MM/AAAA (ej: 20/04/2002).", parent=ventana)
            return

        # Cargamos la lista actual de socios desde 'clientes.json'
        socios = cargar_socios()

        # Validación 4: Comprobar que no exista ya otra persona con el mismo número de DNI
        if any(s.dni == dni for s in socios):
            messagebox.showerror("Error", f"Ya existe un socio registrado con el DNI {dni}.", parent=ventana)
            return

        # Convertimos la opción elegida en el desplegable a un valor booleano (True si dice "Sí", False si no)
        tiene_apto = True if "Sí" in opcion_apto else False

        # Creamos el nuevo objeto 'Socio' usando el molde definido en 'datos.py'
        nuevo_socio = Socio(
            dni=dni,
            nombre=nombre,
            apellido=apellido,
            fecha_de_nacimiento=fecha,
            clase=clase,
            turno=turno,
            apto_medico=tiene_apto
        )

        # Agregamos el nuevo socio a la lista y guardamos la lista actualizada en 'clientes.json'
        socios.append(nuevo_socio)
        guardar_socios(socios)

        # Armamos el mensaje de confirmación para el usuario
        mensaje_exito = f"Socio {nombre} {apellido} registrado con éxito.\nActividad: {clase} | Turno: {turno}."
        if clase in ("Natación", "Ambas") and not tiene_apto:
            mensaje_exito += "\n\n⚠️ Recordatorio: Solicitar certificado médico antes del ingreso al agua."

        messagebox.showinfo("Éxito", mensaje_exito, parent=ventana)

        # Si nos pasaron la función para actualizar la pantalla principal, la ejecutamos ahora
        if callback_actualizar:
            callback_actualizar()

        # Cerramos la ventana de alta porque el socio ya quedó guardado
        ventana.destroy()

    # --- FILA 7: Contenedor y Botones de Guardar / Cancelar ---
    frame_botones = ttk.Frame(frame, style="Card.TFrame")
    frame_botones.grid(row=7, column=0, columnspan=2, pady=(16, 4))

    # Botón para confirmar y guardar el nuevo socio
    btn_guardar = ttk.Button(frame_botones, text="💾 Guardar Socio", command=guardar)
    btn_guardar.pack(side="left", padx=6)

    # Botón para cerrar la ventana sin guardar cambios
    btn_cancelar = ttk.Button(frame_botones, text="Cancelar", command=ventana.destroy)
    btn_cancelar.pack(side="left", padx=6)
