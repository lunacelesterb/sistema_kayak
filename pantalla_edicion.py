"""
================================================================================
ARCHIVO: pantalla_edicion.py (Modificación de Datos de un Alumno Existente)
================================================================================

1. PROPÓSITO GENERAL:
   Este módulo se abre cuando seleccionás a un alumno en la tabla de estadísticas y
   presionás "✏️ Modificar Alumno" (o hacés doble clic sobre su fila). Su propósito
   en la práctica es permitir corregir o actualizar cualquier dato del socio (nombre,
   apellido, fecha de nacimiento, cambio de actividad, cambio de turno, entrega del
   apto médico o baja a estado "Inactivo") y guardar los cambios en 'clientes.json'.

2. ELEMENTOS VISUALES / INTERFAZ:
   - Ventana Secundaria ('ventana = tk.Toplevel'): Mide 480x530 píxeles, es modal y
     muestra la imagen 'fondo.jpg' difuminada de fondo.
   - Botón Conmutador de Tema (🌙 / ☀️): Arriba a la derecha.
   - Tarjeta de Edición ('frame = ttk.LabelFrame'): Cuadro con marco Azul Glicina
     (#779be7) organizado en una cuadrícula ('grid') de 9 filas:
     * Campo DNI ('entry_dni'): Deshabilitado ('state="disabled"') para que se vea a
       quién se está editando sin riesgo de alterar su identificador único.
     * 3 Cajas de texto ('ttk.Entry' de ancho 22): Nombre, Apellido y Fecha de Nacimiento,
       ya rellenadas con los datos actuales del socio.
     * 4 Listas desplegables ('ttk.Combobox' de ancho 19): Actividad, Turno, Apto Médico
       y Estado (Activo / Inactivo), también preseleccionadas con los valores actuales.
   - Botones ('💾 Guardar Cambios' y 'Cancelar'): Con inversión de color en Hover a
     Cielo Fresco (#49b6ff) y crecimiento de fuente al hacer clic.

3. EXPLICACIÓN LÍNEA POR LÍNEA:
   Cada instrucción está comentada debajo en lenguaje llano.
================================================================================
"""

# Aquí importamos 'tkinter', 'ttk' y 'messagebox' para la interfaz gráfica y mensajes de aviso
import tkinter as tk
from tkinter import ttk, messagebox
# Aquí importamos 'datetime' para validar que la fecha de nacimiento editada sea correcta
from datetime import datetime
# Aquí importamos la función que actualiza el JSON y las funciones de diseño desde 'logica.py'
from logica import (
    actualizar_socio,
    configurar_estilos_modernos,
    crear_boton_tema
)


def abrir(root, socio, callback_actualizar=None):
    """
    Abre una ventana emergente modal con los datos precargados del 'socio' elegido.
    """
    # Verificación de seguridad: si no se recibió ningún objeto socio, avisa y no abre la ventana
    if not socio:
        messagebox.showwarning("Atención", "No se especificó ningún alumno para modificar.")
        return

    # Aquí se crea la ventana secundaria indicando en el título el DNI del alumno que se edita
    ventana = tk.Toplevel(root)
    ventana.title(f"Modificar Alumno - DNI: {socio.dni}")
    # Aquí se define el tamaño de la ventana: 480 píxeles de ancho por 530 píxeles de alto
    ventana.geometry("480x530")
    ventana.resizable(False, False)
    ventana.grab_set()

    # Aquí aplicamos el fondo difuminado y los estilos de colores azules
    configurar_estilos_modernos(ventana)
    # Aquí colocamos arriba a la derecha el botón para alternar entre Modo Día y Modo Noche
    crear_boton_tema(ventana, padx=18, pady=(10, 2))

    # Aquí creamos la tarjeta principal ('LabelFrame') mostrando el nombre del socio en el título
    frame = ttk.LabelFrame(
        ventana,
        text=f" ✏️ Editando Socio: {socio.nombre} {socio.apellido} ",
        padding=15
    )
    frame.pack(fill="both", expand=True, padx=18, pady=(4, 16))

    # --- FILA 0: DNI (Protegido contra cambios accidentales) ---
    ttk.Label(frame, text="DNI:", style="Card.TLabel").grid(row=0, column=0, padx=8, pady=6, sticky="e")
    entry_dni = ttk.Entry(frame, width=22)
    entry_dni.grid(row=0, column=1, padx=8, pady=6, sticky="w")
    # Primero escribimos el DNI actual dentro de la caja de texto
    entry_dni.insert(0, str(socio.dni))
    # Luego bloqueamos la caja ('state="disabled"') para que nadie pueda borrar ni cambiar el DNI
    entry_dni.config(state="disabled")

    # --- FILA 1: Nombre (Precargado con el nombre actual) ---
    ttk.Label(frame, text="Nombre:", style="Card.TLabel").grid(row=1, column=0, padx=8, pady=6, sticky="e")
    entry_nombre = ttk.Entry(frame, width=22)
    entry_nombre.grid(row=1, column=1, padx=8, pady=6, sticky="w")
    entry_nombre.insert(0, socio.nombre)

    # --- FILA 2: Apellido (Precargado con el apellido actual) ---
    ttk.Label(frame, text="Apellido:", style="Card.TLabel").grid(row=2, column=0, padx=8, pady=6, sticky="e")
    entry_apellido = ttk.Entry(frame, width=22)
    entry_apellido.grid(row=2, column=1, padx=8, pady=6, sticky="w")
    entry_apellido.insert(0, socio.apellido)

    # --- FILA 3: Fecha de Nacimiento (Precargada) ---
    ttk.Label(frame, text="F. Nac. (DD/MM/AAAA):", style="Card.TLabel").grid(row=3, column=0, padx=8, pady=6, sticky="e")
    entry_fecha = ttk.Entry(frame, width=22)
    entry_fecha.grid(row=3, column=1, padx=8, pady=6, sticky="w")
    entry_fecha.insert(0, str(socio.nacimiento))

    # --- FILA 4: Actividad (Desplegable preseleccionado) ---
    ttk.Label(frame, text="Actividad:", style="Card.TLabel").grid(row=4, column=0, padx=8, pady=6, sticky="e")
    combo_clase = ttk.Combobox(
        frame,
        values=["Kayak", "Natación", "Ambas"],
        state="readonly",
        width=19
    )
    combo_clase.grid(row=4, column=1, padx=8, pady=6, sticky="w")
    combo_clase.set(socio.clase if socio.clase in ("Kayak", "Natación", "Ambas") else "Kayak")

    # --- FILA 5: Turno (Desplegable preseleccionado) ---
    ttk.Label(frame, text="Turno:", style="Card.TLabel").grid(row=5, column=0, padx=8, pady=6, sticky="e")
    combo_turno = ttk.Combobox(
        frame,
        values=["Mañana", "Tarde"],
        state="readonly",
        width=19
    )
    combo_turno.grid(row=5, column=1, padx=8, pady=6, sticky="w")
    combo_turno.set(socio.turno if socio.turno in ("Mañana", "Tarde") else "Mañana")

    # --- FILA 6: Apto Médico ---
    ttk.Label(frame, text="Apto Médico:", style="Card.TLabel").grid(row=6, column=0, padx=8, pady=6, sticky="e")
    combo_apto = ttk.Combobox(
        frame,
        values=["Sí (Entregado)", "No (Pendiente)", "No requiere"],
        state="readonly",
        width=19
    )
    combo_apto.grid(row=6, column=1, padx=8, pady=6, sticky="w")

    # Según la actividad actual del socio, mostramos si no requiere apto o si ya lo entregó
    if combo_clase.get() == "Kayak":
        combo_apto.set("No requiere")
    else:
        combo_apto.set("Sí (Entregado)" if socio.apto_medico else "No (Pendiente)")

    # Aquí se maneja lo que pasa si el usuario cambia la actividad durante la edición:
    def al_cambiar_actividad(event=None):
        actividad = combo_clase.get()
        if actividad in ("Natación", "Ambas"):
            combo_apto.config(values=["Sí (Entregado)", "No (Pendiente)"])
            combo_apto.set("Sí (Entregado)" if socio.apto_medico else "No (Pendiente)")
        else:
            combo_apto.config(values=["No requiere"])
            combo_apto.set("No requiere")

    combo_clase.bind("<<ComboboxSelected>>", al_cambiar_actividad)

    # --- FILA 7: Estado del Socio (Activo o Inactivo) ---
    ttk.Label(frame, text="Estado:", style="Card.TLabel").grid(row=7, column=0, padx=8, pady=6, sticky="e")
    combo_estado = ttk.Combobox(
        frame,
        values=["Activo", "Inactivo"],
        state="readonly",
        width=19
    )
    combo_estado.grid(row=7, column=1, padx=8, pady=6, sticky="w")
    combo_estado.set(socio.estado if socio.estado in ("Activo", "Inactivo") else "Activo")

    # Aquí se maneja lo que pasa cuando el usuario hace clic en "💾 Guardar Cambios":
    def guardar():
        # Leemos todos los valores nuevos de los campos
        nombre = entry_nombre.get().strip()
        apellido = entry_apellido.get().strip()
        fecha = entry_fecha.get().strip()
        clase = combo_clase.get()
        turno = combo_turno.get()
        opcion_apto = combo_apto.get()
        estado = combo_estado.get()

        # Validamos que no haya borrado el nombre, apellido o fecha
        if not nombre or not apellido or not fecha:
            messagebox.showwarning("Atención", "Complete todos los campos de texto.", parent=ventana)
            return

        # Validamos que la fecha siga respetando el formato DD/MM/AAAA
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "La fecha debe tener el formato DD/MM/AAAA.", parent=ventana)
            return

        tiene_apto = True if "Sí" in opcion_apto else False

        # Armamos un diccionario con todos los datos modificados
        datos_nuevos = {
            "nombre": nombre,
            "apellido": apellido,
            "nacimiento": fecha,
            "clase": clase,
            "turno": turno,
            "apto_medico": tiene_apto,
            "estado": estado
        }

        # Llamamos a 'actualizar_socio' en 'logica.py' para que guarde los cambios en 'clientes.json'
        exito = actualizar_socio(socio.dni, datos_nuevos)
        if exito:
            messagebox.showinfo(
                "Modificación Exitosa",
                f"Los datos de {nombre} {apellido} fueron actualizados correctamente.",
                parent=ventana
            )
            # Refrescamos la tabla de atrás y la ventana principal
            if callback_actualizar:
                callback_actualizar()
            ventana.destroy()
        else:
            messagebox.showerror("Error", "No se pudo actualizar el registro.", parent=ventana)

    # --- FILA 8: Botones de Guardar y Cancelar ---
    frame_botones = ttk.Frame(frame, style="Card.TFrame")
    frame_botones.grid(row=8, column=0, columnspan=2, pady=(16, 4))

    btn_guardar = ttk.Button(frame_botones, text="💾 Guardar Cambios", command=guardar)
    btn_guardar.pack(side="left", padx=6)

    btn_cancelar = ttk.Button(frame_botones, text="Cancelar", command=ventana.destroy)
    btn_cancelar.pack(side="left", padx=6)
