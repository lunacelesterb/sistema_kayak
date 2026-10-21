"""
================================================================================
ARCHIVO: pantalla_estadisticas.py (Panel de Consultas, Tabla, Gestión y Reportes PDF)
================================================================================

1. PROPÓSITO GENERAL:
   Es el panel de control administrativo completo del club. Permite ver las métricas
   generales y el dinero recaudado en el mes, buscar alumnos en tiempo real a medida
   que se escribe, filtrar el listado por categoría (para avisar, atrasados, al día,
   apto pendiente o turnos), editar a un alumno, eliminar a uno o varios alumnos al
   mismo tiempo y descargar los reportes institucionales en formato PDF.

2. ELEMENTOS VISUALES / INTERFAZ:
   - Ventana Secundaria ('ventana = tk.Toplevel'): Mide 960x680 píxeles (mínimo 850x590),
     redimensionable y con imagen 'fondo.jpg' difuminada de fondo.
   - Botón Conmutador de Tema (🌙 / ☀️): Ubicado arriba a la derecha.
   - Tarjeta 1 (" 📊 Resumen del Club y Recaudación Mensual "): Muestra 3 renglones
     con totales por disciplina, por turno e ingresos en pesos del mes.
   - Tarjeta 2 (" 🔍 Búsqueda y Filtros "):
     * Caja de texto ('entry_busqueda' de ancho 20) que filtra instantáneamente al soltar
       cada tecla ('<KeyRelease>').
     * Desplegable ('combo_filtro' de ancho 28) con 7 filtros rápidos.
     * Botón "Limpiar Filtros".
   - Tarjeta 3 (" 📋 Nómina de Alumnos y Acciones "):
     * Tabla Interactiva ('tabla = ttk.Treeview'): Tiene 8 columnas, encabezado en color
       Azul Glicina (#779be7), selección en Cielo Fresco (#49b6ff) y soporte para elegir
       múltiples filas con Ctrl o Shift ('selectmode="extended"').
     * Botonera de gestión: "✏️ Modificar Alumno", "🗑️ Eliminar Alumno(s) Seleccionado(s)",
       "☑️ Seleccionar Todos" y "⬜ Deseleccionar".
     * Botonera de exportación PDF: "📄 Descargar Reporte General (PDF)",
       "⚠️ Descargar Listado de Cobranzas y Avisos (PDF)" y "Cerrar".

3. EXPLICACIÓN LÍNEA POR LÍNEA:
   Cada bloque e instrucción está explicado en lenguaje llano debajo.
================================================================================
"""

# Aquí importamos 'tkinter', 'ttk' y 'messagebox' para construir el panel visual
import tkinter as tk
from tkinter import ttk, messagebox
# Aquí importamos 'os' para abrir automáticamente el archivo PDF recién generado en Windows
import os
# Aquí importamos 'date' para consultar el mes y año actual en el cálculo de recaudación
from datetime import date
# Aquí importamos todas las funciones de consulta, baja múltiple, PDFs y diseño desde 'logica.py'
from logica import (
    cargar_socios,
    eliminar_socios_multiples,
    calcular_estadisticas,
    calcular_recaudacion_mes,
    filtrar_socios,
    generar_reporte_pdf,
    generar_reporte_avisos_pdf,
    configurar_estilos_modernos,
    crear_boton_tema
)
# Aquí importamos 'pantalla_edicion' para poder abrirla cuando se quiera modificar a un alumno
import pantalla_edicion


def abrir(root, callback_actualizar=None):
    """
    Construye y muestra el panel general de consultas, tabla interactiva y reportes PDF.
    """
    # Aquí se crea la ventana secundaria amplia (960x680 píxeles)
    ventana = tk.Toplevel(root)
    ventana.title("Panel de Consultas, Gestión de Alumnos y Reportes - Sistema Náutico")
    ventana.geometry("960x680")
    ventana.minsize(850, 590)

    # Aquí se aplica el fondo difuminado, la paleta de tonos azules y los efectos de botones
    configurar_estilos_modernos(ventana)
    # Aquí se coloca arriba a la derecha el botón 🌙 / ☀️ para alternar entre Modo Día y Modo Noche
    crear_boton_tema(ventana, padx=16, pady=(8, 2))

    # ----------------------------------------------------
    # 1. Tarjeta de Resumen de Métricas e Ingresos por Mes
    # ----------------------------------------------------
    frame_kpi = ttk.LabelFrame(ventana, text=" 📊 Resumen del Club y Recaudación Mensual ", padding=10)
    frame_kpi.pack(fill="x", padx=16, pady=4)

    # Tres etiquetas para mostrar los indicadores clave del club
    lbl_kpi_alumnos = ttk.Label(frame_kpi, text="", style="Card.TLabel")
    lbl_kpi_alumnos.pack(anchor="w", pady=1)

    lbl_kpi_turnos = ttk.Label(frame_kpi, text="", style="Card.TLabel")
    lbl_kpi_turnos.pack(anchor="w", pady=1)

    lbl_kpi_dinero = ttk.Label(
        frame_kpi,
        text="",
        style="Accent.Card.TLabel"
    )
    lbl_kpi_dinero.pack(anchor="w", pady=(3, 0))

    # Función que recalcula y escribe los totales en las 3 etiquetas superiores
    def actualizar_tarjetas(socios):
        stats = calcular_estadisticas(socios)
        hoy = date.today()
        periodo_actual = f"{hoy.month:02d}/{hoy.year}"
        recaudacion = calcular_recaudacion_mes(periodo=periodo_actual, socios=socios)

        lbl_kpi_alumnos.config(
            text=f"Total de Alumnos: {stats['total']}  |  Kayak: {stats['kayak']}  |  "
                 f"Natación: {stats['natacion']}  |  Ambas actividades: {stats['ambas']}"
        )
        lbl_kpi_turnos.config(
            text=f"Turno Mañana: {stats['turno_manana']}  |  Turno Tarde: {stats['turno_tarde']}  |  "
                 f"Aptos médicos pendientes: {stats['apto_pendiente']}"
        )
        lbl_kpi_dinero.config(
            text=f"💰 Ingresos por Cuotas ({periodo_actual}): ${recaudacion['total_recaudado']:,.2f}  "
                 f"({recaudacion['cantidad_pagos']} pagos registrados)  |  "
                 f"Cuotas al día: {stats['al_dia']}  |  Pendientes/Atrasadas: {stats['pendientes'] + stats['atrasados']}"
        )

    # ----------------------------------------------------
    # 2. Tarjeta de Búsqueda en Vivo y Filtros Rápidos
    # ----------------------------------------------------
    frame_filtros = ttk.LabelFrame(ventana, text=" 🔍 Búsqueda y Filtros ", padding=8)
    frame_filtros.pack(fill="x", padx=16, pady=4)

    ttk.Label(frame_filtros, text="Buscar (DNI o Nombre):", style="Card.TLabel").pack(side="left", padx=(4, 4))
    entry_busqueda = ttk.Entry(frame_filtros, width=20)
    entry_busqueda.pack(side="left", padx=(0, 12))

    ttk.Label(frame_filtros, text="Filtrar por:", style="Card.TLabel").pack(side="left", padx=(4, 4))
    # Lista con las 7 opciones de filtrado disponibles
    opciones_filtro = [
        "Todos los socios",
        "Para avisar (Sin pago este mes)",
        "Atrasados (Morosos post día 10)",
        "Al día",
        "Con Apto Médico pendiente",
        "Turno Mañana",
        "Turno Tarde"
    ]
    combo_filtro = ttk.Combobox(frame_filtros, values=opciones_filtro, state="readonly", width=28)
    combo_filtro.pack(side="left", padx=4)
    combo_filtro.current(0)

    # Botón que borra el texto buscado, vuelve el filtro a "Todos los socios" y recarga la tabla
    btn_limpiar = ttk.Button(
        frame_filtros,
        text="Limpiar Filtros",
        command=lambda: [entry_busqueda.delete(0, tk.END), combo_filtro.current(0), cargar_datos_tabla()]
    )
    btn_limpiar.pack(side="left", padx=8)

    # ----------------------------------------------------
    # 3. Tarjeta de Tabla Interactiva (ttk.Treeview) y Acciones
    # ----------------------------------------------------
    frame_panel_tabla = ttk.LabelFrame(ventana, text=" 📋 Nómina de Alumnos y Acciones ", padding=10)
    frame_panel_tabla.pack(fill="both", expand=True, padx=16, pady=(4, 14))

    frame_tabla = ttk.Frame(frame_panel_tabla, style="Card.TFrame")
    frame_tabla.pack(fill="both", expand=True, pady=(0, 6))

    # Aquí se definen los nombres internos de las 8 columnas de la tabla
    columnas = ("dni", "nombre", "clase", "turno", "estado_cuota", "periodo", "apto", "estado")
    # 'show="headings"' muestra solo nuestras columnas con título; 'selectmode="extended"' permite elegir varias filas
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=11, selectmode="extended")

    # Aquí se definen los títulos visibles en el encabezado de cada columna
    tabla.heading("dni", text="DNI")
    tabla.heading("nombre", text="Apellido y Nombre")
    tabla.heading("clase", text="Actividad")
    tabla.heading("turno", text="Turno")
    tabla.heading("estado_cuota", text="Estado Cuota")
    tabla.heading("periodo", text="Período")
    tabla.heading("apto", text="Apto Médico")
    tabla.heading("estado", text="Estado")

    # Aquí se define el ancho en píxeles y la alineación ("center" = centrado, "w" = izquierda) de cada columna
    tabla.column("dni", width=80, anchor="center")
    tabla.column("nombre", width=180, anchor="w")
    tabla.column("clase", width=95, anchor="center")
    tabla.column("turno", width=80, anchor="center")
    tabla.column("estado_cuota", width=145, anchor="center")
    tabla.column("periodo", width=90, anchor="center")
    tabla.column("apto", width=95, anchor="center")
    tabla.column("estado", width=80, anchor="center")

    # Barra de desplazamiento vertical conectada a la tabla
    scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scroll_y.set)
    tabla.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

    # Función que vacía la tabla y la vuelve a llenar según el texto buscado y el filtro elegido
    def cargar_datos_tabla(event=None):
        # 1. Borramos todos los renglones actuales de la tabla visual para no duplicarlos
        for item in tabla.get_children():
            tabla.delete(item)

        # 2. Leemos los socios desde 'clientes.json' y actualizamos la tarjeta superior
        socios = cargar_socios()
        actualizar_tarjetas(socios)

        # 3. Aplicamos el buscador y el filtro seleccionados
        texto = entry_busqueda.get()
        filtro = combo_filtro.get()
        socios_filtrados = filtrar_socios(texto_busqueda=texto, filtro_estado=filtro, socios=socios)

        # 4. Insertamos cada socio filtrado como una fila nueva en la tabla
        for s in socios_filtrados:
            nombre_completo = f"{s.apellido}, {s.nombre}"
            estado_cuota = s.obtener_estado_cuota()

            if s.actividad.requiere_apto:
                apto_texto = "Sí" if s.apto_medico else "Falta"
            else:
                apto_texto = "No req."

            tabla.insert(
                "",
                "end",
                values=(
                    s.dni,
                    nombre_completo,
                    s.clase,
                    s.turno,
                    estado_cuota,
                    s.periodo_abonado or "-",
                    apto_texto,
                    s.estado
                )
            )

    # Aquí conectamos los filtros en tiempo real:
    # '<<ComboboxSelected>>' recarga la tabla al cambiar el filtro desplegable
    combo_filtro.bind("<<ComboboxSelected>>", cargar_datos_tabla)
    # '<KeyRelease>' recarga la tabla instantáneamente cada vez que el usuario escribe una letra en el buscador
    entry_busqueda.bind("<KeyRelease>", cargar_datos_tabla)

    # ----------------------------------------------------
    # 4. Operaciones sobre Alumnos: Modificar y Borrado Múltiple
    # ----------------------------------------------------
    frame_gestion = ttk.Frame(frame_panel_tabla, style="Card.TFrame")
    frame_gestion.pack(fill="x", pady=4)

    def obtener_socios_seleccionados():
        """
        Revisa qué filas de la tabla están pintadas/seleccionadas por el usuario
        y devuelve la lista de objetos 'Socio' correspondientes.
        """
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning(
                "Seleccionar Alumno(s)",
                "Por favor, seleccione al menos un alumno de la tabla.\n\n"
                "Tip: Puede mantener presionada la tecla Ctrl o Shift y hacer clic sobre varios alumnos para seleccionarlos a la vez.",
                parent=ventana
            )
            return []

        socios = cargar_socios()
        socios_dict = {str(s.dni).strip(): s for s in socios}
        resultado = []

        for item_id in seleccion:
            item = tabla.item(item_id)
            dni = str(item["values"][0]).strip()
            if dni in socios_dict:
                resultado.append(socios_dict[dni])

        return resultado

    # Aquí se maneja lo que pasa cuando el usuario hace clic en "✏️ Modificar Alumno" (o doble clic en la tabla):
    def modificar_alumno():
        seleccionados = obtener_socios_seleccionados()
        if not seleccionados:
            return

        # Solo se puede editar 1 alumno por vez
        if len(seleccionados) > 1:
            messagebox.showinfo(
                "Modificación Individual",
                "Para modificar datos, por favor seleccione un único alumno a la vez.",
                parent=ventana
            )
            return

        socio = seleccionados[0]
        def refrescar_todo():
            cargar_datos_tabla()
            if callback_actualizar:
                callback_actualizar()
        # Abrimos la ventana 'pantalla_edicion.py' pasándole el socio seleccionado
        pantalla_edicion.abrir(ventana, socio, callback_actualizar=refrescar_todo)

    # Aquí se maneja lo que pasa cuando el usuario hace clic en "🗑️ Eliminar Alumno(s) Seleccionado(s)":
    def eliminar_alumnos_seleccionados():
        seleccionados = obtener_socios_seleccionados()
        if not seleccionados:
            return

        cant = len(seleccionados)

        # Armamos la pregunta de confirmación según si se va a borrar a 1 solo alumno o a varios en bloque
        if cant == 1:
            socio = seleccionados[0]
            pregunta = (
                f"¿Está seguro de que desea eliminar al alumno:\n\n"
                f"• Nombre: {socio.nombre} {socio.apellido}\n"
                f"• DNI: {socio.dni}\n"
                f"• Actividad: {socio.clase} (Turno: {socio.turno})\n\n"
                f"Esta acción borrará definitivamente sus registros."
            )
            titulo_alerta = "Confirmar Eliminación"
        else:
            lineas_socios = [f"• {s.nombre} {s.apellido} (DNI: {s.dni} - {s.clase})" for s in seleccionados[:6]]
            texto_lista = "\n".join(lineas_socios)
            if cant > 6:
                texto_lista += f"\n... y {cant - 6} alumnos más."

            pregunta = (
                f"¿Está seguro de que desea eliminar a los {cant} alumnos seleccionados?\n\n"
                f"Alumnos a eliminar:\n{texto_lista}\n\n"
                f"Esta acción borrará definitivamente los registros de todos ellos."
            )
            titulo_alerta = f"Confirmar Eliminación Múltiple ({cant} Alumnos)"

        # Mostramos el cuadro de confirmación Sí / No
        confirmado = messagebox.askyesno(
            titulo_alerta,
            pregunta,
            parent=ventana
        )

        # Si el usuario confirma que Sí, borramos esos DNIs de 'clientes.json' y refrescamos la pantalla
        if confirmado:
            dnis = [s.dni for s in seleccionados]
            cant_eliminados = eliminar_socios_multiples(dnis)
            messagebox.showinfo(
                "Eliminación Exitosa",
                f"Se {'eliminaron' if cant_eliminados > 1 else 'eliminó'} correctamente a {cant_eliminados} {'alumnos' if cant_eliminados > 1 else 'alumno'}.",
                parent=ventana
            )
            cargar_datos_tabla()
            if callback_actualizar:
                callback_actualizar()

    # Funciones para pintar o despintar todas las filas de la tabla con un solo clic
    def seleccionar_todos():
        todos = tabla.get_children()
        tabla.selection_set(todos)

    def deseleccionar_todos():
        tabla.selection_remove(tabla.selection())

    # Botones de acción sobre la tabla
    btn_modificar = ttk.Button(frame_gestion, text="✏️ Modificar Alumno", command=modificar_alumno)
    btn_modificar.pack(side="left", padx=4)

    btn_eliminar = ttk.Button(frame_gestion, text="🗑️ Eliminar Alumno(s) Seleccionado(s)", command=eliminar_alumnos_seleccionados)
    btn_eliminar.pack(side="left", padx=4)

    btn_sel_todos = ttk.Button(frame_gestion, text="☑️ Seleccionar Todos", command=seleccionar_todos)
    btn_sel_todos.pack(side="left", padx=4)

    btn_desel = ttk.Button(frame_gestion, text="⬜ Deseleccionar", command=deseleccionar_todos)
    btn_desel.pack(side="left", padx=4)

    ttk.Label(
        frame_gestion,
        text="(Ctrl + Clic o Shift + Clic para seleccionar múltiples)",
        style="Muted.Card.TLabel"
    ).pack(side="left", padx=8)

    # Permite abrir la edición haciendo doble clic izquierdo ("<Double-1>") sobre cualquier fila
    tabla.bind("<Double-1>", lambda event: modificar_alumno())

    # Llenamos la tabla al abrir la ventana
    cargar_datos_tabla()

    # ----------------------------------------------------
    # 5. Botones de Exportación PDF y Cierre
    # ----------------------------------------------------
    frame_acciones = ttk.Frame(frame_panel_tabla, style="Card.TFrame")
    frame_acciones.pack(fill="x", pady=(6, 0))

    # Aquí se maneja la descarga y apertura automática del Reporte General en PDF
    def exportar_general():
        socios = cargar_socios()
        if not socios:
            messagebox.showwarning("Atención", "No hay datos de socios para exportar.", parent=ventana)
            return
        ruta = generar_reporte_pdf(socios)
        messagebox.showinfo(
            "Reporte Generado con Éxito",
            f"El Reporte General en PDF se guardó en:\n{ruta}",
            parent=ventana
        )
        # 'os.startfile(ruta)' abre automáticamente el PDF en el visor de documentos de Windows
        try:
            os.startfile(ruta)
        except Exception:
            pass

    # Aquí se maneja la descarga y apertura del Listado de Cobranzas y Avisos en PDF
    def exportar_avisos():
        socios = cargar_socios()
        if not socios:
            messagebox.showwarning("Atención", "No hay socios registrados.", parent=ventana)
            return
        ruta = generar_reporte_avisos_pdf(socios)
        messagebox.showinfo(
            "Listado de Cobranzas Generado",
            f"El Listado de Avisos y Cobranzas se guardó en:\n{ruta}",
            parent=ventana
        )
        try:
            os.startfile(ruta)
        except Exception:
            pass

    btn_pdf_gral = ttk.Button(frame_acciones, text="📄 Descargar Reporte General (PDF)", command=exportar_general)
    btn_pdf_gral.pack(side="left", padx=4)

    btn_pdf_avisos = ttk.Button(frame_acciones, text="⚠️ Descargar Listado de Cobranzas y Avisos (PDF)", command=exportar_avisos)
    btn_pdf_avisos.pack(side="left", padx=4)

    btn_cerrar = ttk.Button(frame_acciones, text="Cerrar", command=ventana.destroy)
    btn_cerrar.pack(side="right", padx=4)
