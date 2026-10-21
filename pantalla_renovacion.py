"""
================================================================================
ARCHIVO: pantalla_renovacion.py (Cobro de Cuotas y Resolución de Homónimos)
================================================================================

1. PROPÓSITO GENERAL:
   Este módulo gestiona el cobro mensual de cuotas del club. En la práctica, permite
   buscar a cualquier socio por su DNI o por su Nombre. Si existen varias personas con
   el mismo nombre (homónimos, por ejemplo dos socios llamados "Jorge"), el sistema
   despliega automáticamente una lista interactiva con los datos de cada uno para que
   el usuario seleccione al socio correcto con un clic, cargue su arancel automático
   y registre el pago en 'clientes.json'.

2. ELEMENTOS VISUALES / INTERFAZ:
   - Ventana Secundaria ('ventana = tk.Toplevel'): Mide 560x640 píxeles (mínimo 530x590),
     con imagen 'fondo.jpg' difuminada de fondo.
   - Botón Conmutador de Tema (🌙 / ☀️): Ubicado arriba a la derecha.
   - Tarjeta 1 (" 1. Búsqueda y Selección del Socio "):
     * Caja de búsqueda ('entry_busqueda' de ancho 24) y botón "🔍 Buscar Socio".
     * Panel Dinámico de Homónimos ('frame_homonimos'): Permanece oculto si hay un solo
       resultado, y se despliega automáticamente cuando hay múltiples coincidencias.
       Contiene una lista desplegable ('combo_coincidencias' de ancho 52) y un cuadro
       de lista ('listbox_coincidencias' de 4 filas de alto con barra de scroll y
       selección en color Cielo Fresco #49b6ff).
     * Etiqueta informativa ('lbl_datos_socio'): Muestra el nombre, DNI, actividad,
       turno, arancel sugerido y estado de cuota del socio seleccionado.
   - Tarjeta 2 (" 2. Detalles del Período e Importe a Cobrar "):
     * Lista desplegable de Mes ("01 - Enero" a "12 - Diciembre").
     * Cajas de texto para Año, Fecha de pago (DD/MM/AAAA) e Importe cobrado ($).
     * Botones "💳 Confirmar y Cobrar Cuota" y "Cancelar".

3. EXPLICACIÓN LÍNEA POR LÍNEA:
   Cada bloque e instrucción está detallado en lenguaje llano debajo.
================================================================================
"""

# Aquí importamos 'tkinter', 'ttk' y 'messagebox' para crear los controles gráficos y avisos
import tkinter as tk
from tkinter import ttk, messagebox
# Aquí importamos 'date' y 'datetime' para precompletar la fecha de hoy y validarla
from datetime import date, datetime
# Aquí importamos las funciones de búsqueda de homónimos, persistencia y diseño desde 'logica.py'
from logica import (
    cargar_socios,
    guardar_socios,
    buscar_socios_coincidentes,
    configurar_estilos_modernos,
    crear_boton_tema,
    obtener_tema_actual,
    COLOR_CIELO_FRESCO,
    FUENTE_PRINCIPAL
)


def abrir(root, callback_actualizar=None):
    """
    Abre la ventana emergente para buscar a un socio (resolviendo homónimos) y cobrar su cuota.
    """
    # Aquí se crea la ventana secundaria hija de 'root'
    ventana = tk.Toplevel(root)
    ventana.title("Registro de Cobro de Cuota - Sistema Náutico")
    # Aquí se define el tamaño inicial (560x640) y el tamaño mínimo (530x590)
    ventana.geometry("560x640")
    ventana.minsize(530, 590)
    ventana.grab_set()

    # Aquí creamos un diccionario en memoria para recordar qué socio está seleccionado
    # y guardar la lista de coincidencias cuando aparecen homónimos
    estado_busqueda = {
        "socio": None,
        "coincidencias": []
    }

    # Consultamos el tema activo (Modo Día o Modo Noche) para pintar la lista de homónimos
    tema_inicial = obtener_tema_actual()

    # Aquí colocamos arriba a la derecha el botón 🌙 / ☀️ para cambiar entre Modo Día y Modo Noche
    crear_boton_tema(ventana, padx=18, pady=(8, 2))

    # ----------------------------------------------------
    # 1. Tarjeta de Búsqueda y Selección de Homónimos
    # ----------------------------------------------------
    frame_busqueda = ttk.LabelFrame(ventana, text=" 1. Búsqueda y Selección del Socio ", padding=12)
    frame_busqueda.pack(fill="x", padx=18, pady=(2, 8))

    # Renglón superior dentro de la tarjeta 1 para poner la caja de búsqueda y el botón uno al lado del otro
    fila_input = ttk.Frame(frame_busqueda, style="Card.TFrame")
    fila_input.pack(fill="x")

    # Etiqueta "DNI o Nombre:" con fuente Roboto tamaño 9 en negrita
    ttk.Label(
        fila_input,
        text="DNI o Nombre:",
        style="Card.TLabel",
        font=(FUENTE_PRINCIPAL, 9, "bold")
    ).pack(side="left", padx=(0, 8))

    # Caja de texto donde el usuario escribe lo que quiere buscar (ej: "Jorge" o un DNI)
    entry_busqueda = ttk.Entry(fila_input, width=24)
    entry_busqueda.pack(side="left", padx=(0, 8))

    # --- Panel Dinámico de Homónimos ('frame_homonimos') ---
    # Se crea aquí pero NO se le hace '.pack()' todavía: solo se hace visible si hay más de 1 resultado
    frame_homonimos = ttk.Frame(frame_busqueda, style="Card.TFrame")

    # Etiqueta que avisa cuántas personas coincidieron con el nombre buscado
    lbl_aviso_homonimos = ttk.Label(
        frame_homonimos,
        text="Seleccione al socio correspondiente de la lista:",
        style="Accent.Card.TLabel"
    )
    lbl_aviso_homonimos.pack(anchor="w", pady=(8, 4))

    # Menú desplegable ('Combobox') para elegir entre los homónimos encontrados
    combo_coincidencias = ttk.Combobox(frame_homonimos, state="readonly", width=52)
    combo_coincidencias.pack(fill="x", pady=(0, 4))

    # Cuadro de lista abierta ('Listbox') con barra de desplazamiento vertical para ver a todos de un vistazo
    frame_lista = ttk.Frame(frame_homonimos, style="Card.TFrame")
    frame_lista.pack(fill="x")

    scroll_lista = ttk.Scrollbar(frame_lista, orient="vertical")
    # Aquí se configura el color, la fuente y la altura (4 renglones) del cuadro de homónimos
    listbox_coincidencias = tk.Listbox(
        frame_lista,
        height=4,
        font=(FUENTE_PRINCIPAL, 9),
        bg=tema_inicial["listbox_bg"],
        fg=tema_inicial["listbox_fg"],
        selectbackground=COLOR_CIELO_FRESCO,
        selectforeground="#ffffff",
        relief="solid",
        borderwidth=1,
        highlightthickness=0,
        exportselection=False,
        yscrollcommand=scroll_lista.set
    )
    scroll_lista.config(command=listbox_coincidencias.yview)
    listbox_coincidencias.pack(side="left", fill="x", expand=True)
    scroll_lista.pack(side="right", fill="y")

    # Etiqueta inferior de la Tarjeta 1 que muestra los datos del socio elegido
    lbl_datos_socio = ttk.Label(
        frame_busqueda,
        text="Ingrese un DNI o Nombre y presione 'Buscar Socio'.",
        style="Muted.Card.TLabel"
    )
    lbl_datos_socio.pack(anchor="w", pady=(10, 2))

    # ----------------------------------------------------
    # 2. Tarjeta de Detalles del Cobro (Período e Importe)
    # ----------------------------------------------------
    frame_cobro = ttk.LabelFrame(ventana, text=" 2. Detalles del Período e Importe a Cobrar ", padding=12)
    frame_cobro.pack(fill="both", expand=True, padx=18, pady=(0, 14))

    # Lista de los 12 meses del año para seleccionar qué período está abonando el socio
    meses_nombres = [
        "01 - Enero", "02 - Febrero", "03 - Marzo", "04 - Abril",
        "05 - Mayo", "06 - Junio", "07 - Julio", "08 - Agosto",
        "09 - Septiembre", "10 - Octubre", "11 - Noviembre", "12 - Diciembre"
    ]
    hoy = date.today()
    # Como en Python las listas empiezan en la posición 0, Enero es 0, Febrero es 1, etc. (hoy.month - 1)
    mes_actual_idx = hoy.month - 1

    # --- FILA 0: Selector de Mes ---
    ttk.Label(frame_cobro, text="Mes a cobrar:", style="Card.TLabel").grid(row=0, column=0, padx=8, pady=6, sticky="e")
    combo_mes = ttk.Combobox(frame_cobro, values=meses_nombres, state="readonly", width=20)
    combo_mes.grid(row=0, column=1, padx=8, pady=6, sticky="w")
    combo_mes.current(mes_actual_idx)

    # --- FILA 1: Campo Año ---
    ttk.Label(frame_cobro, text="Año:", style="Card.TLabel").grid(row=1, column=0, padx=8, pady=6, sticky="e")
    entry_anio = ttk.Entry(frame_cobro, width=12)
    entry_anio.grid(row=1, column=1, padx=8, pady=6, sticky="w")
    entry_anio.insert(0, str(hoy.year))

    # --- FILA 2: Campo Fecha de Pago ---
    ttk.Label(frame_cobro, text="Fecha de pago (DD/MM/AAAA):", style="Card.TLabel").grid(row=2, column=0, padx=8, pady=6, sticky="e")
    entry_fecha_pago = ttk.Entry(frame_cobro, width=20)
    entry_fecha_pago.grid(row=2, column=1, padx=8, pady=6, sticky="w")
    entry_fecha_pago.insert(0, hoy.strftime("%d/%m/%Y"))

    # --- FILA 3: Campo Importe en Pesos ($) ---
    ttk.Label(frame_cobro, text="Importe cobrado ($):", style="Card.TLabel").grid(row=3, column=0, padx=8, pady=6, sticky="e")
    entry_monto = ttk.Entry(frame_cobro, width=20)
    entry_monto.grid(row=3, column=1, padx=8, pady=6, sticky="w")

    # Aquí se maneja la actualización de colores si el usuario presiona el botón 🌙 / ☀️ en esta ventana:
    def _al_cambiar_tema(tema):
        listbox_coincidencias.configure(
            bg=tema["listbox_bg"],
            fg=tema["listbox_fg"],
            selectbackground=tema["btn_hover_bg"]
        )
        if estado_busqueda["socio"] is not None:
            cargar_datos_de_socio(estado_busqueda["socio"])

    # Aplicamos los estilos visuales y registramos la ventana para el cambio de tema
    configurar_estilos_modernos(ventana, callback_tema=_al_cambiar_tema)

    # Función que toma al socio elegido y completa automáticamente sus datos y el importe de su cuota
    def cargar_datos_de_socio(s):
        # Guardamos al socio elegido como el socio activo para cobrarle
        estado_busqueda["socio"] = s
        estado_actual = s.obtener_estado_cuota()
        tema = obtener_tema_actual()
        es_noche = tema["nombre"] == "nocturno"

        # Elegimos el color del texto informativo según si está al día, pendiente o atrasado
        if estado_actual == "Al día":
            color = "#49b6ff" if es_noche else "#15803d"
        elif "Pendiente" in estado_actual:
            color = "#fbbf24" if es_noche else "#b45309"
        else:
            color = "#ff499e" if es_noche else "#be123c"

        # Consultamos cuánto cuesta hoy la actividad de este socio en 'precios.json'
        arancel = s.obtener_arancel_actual()
        # Borramos lo que hubiera en la caja de importe y escribimos el precio exacto de su actividad
        entry_monto.delete(0, tk.END)
        entry_monto.insert(0, f"{arancel:.2f}")

        # Mostramos todos los datos particulares del socio en la etiqueta informativa
        info = (
            f"✔ Socio seleccionado: {s.nombre} {s.apellido} (DNI: {s.dni})\n"
            f"• Actividad: {s.clase} | Turno: {s.turno} | Arancel sugerido: ${arancel:,.2f}\n"
            f"• Estado actual: {estado_actual} (Último período: {s.periodo_abonado or 'Sin registro'})"
        )
        lbl_datos_socio.config(text=info, foreground=color, font=(FUENTE_PRINCIPAL, 9, "bold"))

    # Aquí se maneja lo que pasa cuando el usuario hace clic sobre un socio en la lista de homónimos ('Listbox'):
    def al_seleccionar_de_listbox(event=None):
        seleccion = listbox_coincidencias.curselection()
        if not seleccion:
            return
        idx = seleccion[0]
        coincidencias = estado_busqueda["coincidencias"]
        if 0 <= idx < len(coincidencias):
            # Sincronizamos también el menú desplegable y cargamos los datos de ese socio
            combo_coincidencias.current(idx)
            cargar_datos_de_socio(coincidencias[idx])

    # Aquí se maneja lo que pasa cuando el usuario elige un homónimo desde el menú desplegable ('Combobox'):
    def al_seleccionar_de_combo(event=None):
        idx = combo_coincidencias.current()
        coincidencias = estado_busqueda["coincidencias"]
        if 0 <= idx < len(coincidencias):
            listbox_coincidencias.selection_clear(0, tk.END)
            listbox_coincidencias.selection_set(idx)
            listbox_coincidencias.see(idx)
            cargar_datos_de_socio(coincidencias[idx])

    # Conectamos los eventos de selección de ambos controles a sus funciones respectivas
    listbox_coincidencias.bind("<<ListboxSelect>>", al_seleccionar_de_listbox)
    combo_coincidencias.bind("<<ComboboxSelected>>", al_seleccionar_de_combo)

    # Aquí se maneja lo que pasa cuando el usuario presiona "🔍 Buscar Socio" o la tecla Enter:
    def buscar(event=None):
        criterio = entry_busqueda.get().strip()
        if not criterio:
            messagebox.showwarning("Atención", "Escriba un DNI o Nombre para buscar.", parent=ventana)
            return

        # Buscamos TODAS las personas que coincidan con el DNI o Nombre ingresado
        socios = cargar_socios()
        coincidencias = buscar_socios_coincidentes(criterio, socios)
        estado_busqueda["coincidencias"] = coincidencias

        # Limpiamos cualquier lista anterior
        listbox_coincidencias.delete(0, tk.END)
        combo_coincidencias.set("")
        combo_coincidencias.config(values=[])

        # CASO 1: No se encontró ningún socio con ese nombre o DNI
        if not coincidencias:
            estado_busqueda["socio"] = None
            frame_homonimos.pack_forget()
            entry_monto.delete(0, tk.END)
            lbl_datos_socio.config(
                text=f"❌ No se encontró ningún socio que coincida con '{criterio}'.",
                foreground="#ff499e",
                font=(FUENTE_PRINCIPAL, 9, "bold")
            )
            return

        # Armamos el texto descriptivo de cada coincidencia: "Jorge Pérez - DNI: 35123456 - Kayak (Mañana)"
        opciones_formateadas = [
            f"{s.nombre} {s.apellido} - DNI: {s.dni} - {s.clase} ({s.turno})"
            for s in coincidencias
        ]
        combo_coincidencias.config(values=opciones_formateadas)
        for texto_op in opciones_formateadas:
            listbox_coincidencias.insert(tk.END, texto_op)

        # CASO 2: Se encontró exactamente 1 sola persona -> la seleccionamos directamente
        if len(coincidencias) == 1:
            frame_homonimos.pack_forget()
            cargar_datos_de_socio(coincidencias[0])
        # CASO 3: Se encontraron 2 o más personas (Homónimos) -> desplegamos la lista para que elija
        else:
            estado_busqueda["socio"] = None
            entry_monto.delete(0, tk.END)
            lbl_aviso_homonimos.config(
                text=f"🔎 Se encontraron {len(coincidencias)} coincidencias para '{criterio}'. Haga clic en el socio correcto:"
            )
            # Hacemos visible el panel de homónimos justo arriba de la etiqueta de datos
            frame_homonimos.pack(fill="x", before=lbl_datos_socio)
            lbl_datos_socio.config(
                text="⚠️ Múltiples socios encontrados. Seleccione uno de la lista superior para cargar su arancel.",
                foreground="#d264b6",
                font=(FUENTE_PRINCIPAL, 9, "italic")
            )

    # Botón para iniciar la búsqueda
    btn_buscar = ttk.Button(fila_input, text="🔍 Buscar Socio", command=buscar)
    btn_buscar.pack(side="left")

    # También permitimos buscar presionando la tecla Enter ("<Return>") en la caja de texto
    entry_busqueda.bind("<Return>", buscar)

    # Aquí se maneja lo que pasa cuando el usuario hace clic en "💳 Confirmar y Cobrar Cuota":
    def registrar_pago():
        s = estado_busqueda["socio"]
        # Si todavía no había seleccionado un socio, intentamos buscar primero
        if s is None:
            buscar()
            s = estado_busqueda["socio"]
            if s is None:
                if len(estado_busqueda["coincidencias"]) > 1:
                    messagebox.showwarning(
                        "Seleccionar Socio",
                        "Hay múltiples socios con ese nombre.\nPor favor, seleccione al socio correcto de la lista desplegada.",
                        parent=ventana
                    )
                else:
                    messagebox.showerror("Error", "Debe buscar y seleccionar un socio primero.", parent=ventana)
                return

        # Leemos los datos del cobro (fecha, año e importe)
        fecha_pago_texto = entry_fecha_pago.get().strip()
        anio_texto = entry_anio.get().strip()
        monto_texto = entry_monto.get().strip().replace(",", ".")

        if not fecha_pago_texto or not anio_texto or not monto_texto:
            messagebox.showwarning("Atención", "Complete todos los campos del cobro.", parent=ventana)
            return

        # Validamos que la fecha de pago tenga formato real DD/MM/AAAA
        try:
            datetime.strptime(fecha_pago_texto, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "La fecha de pago debe tener formato DD/MM/AAAA.", parent=ventana)
            return

        # Validamos que el año sea un número de 4 cifras (ej: 2026)
        if not anio_texto.isdigit() or len(anio_texto) != 4:
            messagebox.showerror("Error", "El año debe contener 4 dígitos (ej: 2026).", parent=ventana)
            return

        # Validamos que el importe cobrado sea un número positivo
        try:
            monto_cobrado = float(monto_texto)
            if monto_cobrado <= 0:
                messagebox.showerror("Error", "El importe debe ser mayor a cero.", parent=ventana)
                return
        except ValueError:
            messagebox.showerror("Error", "El importe debe ser un número válido.", parent=ventana)
            return

        # Buscamos al socio en la lista general por su DNI para registrarle el pago
        socios = cargar_socios()
        socio_a_actualizar = None
        for item in socios:
            if item.dni == s.dni:
                socio_a_actualizar = item
                break

        if not socio_a_actualizar:
            messagebox.showerror("Error", "Error al recuperar los datos del socio.", parent=ventana)
            return

        # Armamos el período en formato "MM/AAAA" (por ejemplo: "10/2026")
        mes_num = combo_mes.current() + 1
        periodo_formateado = f"{mes_num:02d}/{anio_texto}"

        # Llamamos al método 'registrar_pago' del objeto Socio
        socio_a_actualizar.registrar_pago(
            periodo=periodo_formateado,
            fecha_pago=fecha_pago_texto,
            monto=monto_cobrado
        )

        # Guardamos la lista actualizada en 'clientes.json'
        guardar_socios(socios)

        nuevo_estado = socio_a_actualizar.obtener_estado_cuota()
        messagebox.showinfo(
            "Cobro Registrado con Éxito",
            f"Se registró el cobro para {socio_a_actualizar.nombre} {socio_a_actualizar.apellido} (DNI: {socio_a_actualizar.dni}).\n\n"
            f"• Período abonado: {periodo_formateado}\n"
            f"• Fecha de cobro: {fecha_pago_texto}\n"
            f"• Importe ingresado: ${monto_cobrado:,.2f}\n"
            f"• Estado de cuota: {nuevo_estado}",
            parent=ventana
        )

        # Actualizamos el resumen de la ventana principal y cerramos esta ventana
        if callback_actualizar:
            callback_actualizar()

        ventana.destroy()

    # --- FILA 4: Botones de Confirmar Cobro y Cancelar ---
    frame_botones = ttk.Frame(frame_cobro, style="Card.TFrame")
    frame_botones.grid(row=4, column=0, columnspan=2, pady=(16, 4))

    btn_registrar = ttk.Button(frame_botones, text="💳 Confirmar y Cobrar Cuota", command=registrar_pago)
    btn_registrar.pack(side="left", padx=6)

    btn_cancelar = ttk.Button(frame_botones, text="Cancelar", command=ventana.destroy)
    btn_cancelar.pack(side="left", padx=6)
