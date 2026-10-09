"""
Módulo de Interfaz Gráfica - Consultas, Estadísticas, Edición y Reportes
Permite buscar alumnos por DNI o Nombre, modificar sus datos, eliminarlos,
filtrar por turnos y situaciones de pago, consultar recaudación y exportar reportes en PDF.
"""
import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import date
from logica import (
    cargar_socios,
    buscar_socio,
    eliminar_socio,
    calcular_estadisticas,
    calcular_recaudacion_mes,
    filtrar_socios,
    generar_reporte_pdf,
    generar_reporte_avisos_pdf
)
import pantalla_edicion


def abrir(root, callback_actualizar=None):
    """
    Abre la ventana de consultas avanzadas, gestión completa (modificar/eliminar) y reportes.
    """
    ventana = tk.Toplevel(root)
    ventana.title("Panel de Consultas, Gestión de Alumnos y Reportes - Sistema Náutico")
    ventana.geometry("900x620")
    ventana.minsize(800, 540)

    contenedor = ttk.Frame(ventana, padding=12)
    contenedor.pack(fill="both", expand=True)

    # ----------------------------------------------------
    # 1. Resumen de Métricas e Ingresos por Mes
    # ----------------------------------------------------
    frame_kpi = ttk.LabelFrame(contenedor, text=" Resumen del Club y Recaudación Mensual ", padding=8)
    frame_kpi.pack(fill="x", padx=4, pady=4)

    lbl_kpi_alumnos = ttk.Label(frame_kpi, text="", font=("Segoe UI", 9))
    lbl_kpi_alumnos.pack(anchor="w", pady=1)

    lbl_kpi_turnos = ttk.Label(frame_kpi, text="", font=("Segoe UI", 9))
    lbl_kpi_turnos.pack(anchor="w", pady=1)

    lbl_kpi_dinero = ttk.Label(frame_kpi, text="", font=("Segoe UI", 9, "bold"), foreground="#1b365d")
    lbl_kpi_dinero.pack(anchor="w", pady=(2, 0))

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
    # 2. Barra de Búsqueda por Nombre/DNI y Filtros
    # ----------------------------------------------------
    frame_filtros = ttk.LabelFrame(contenedor, text=" Búsqueda y Filtros ", padding=6)
    frame_filtros.pack(fill="x", padx=4, pady=4)

    ttk.Label(frame_filtros, text="Buscar (DNI o Nombre):").pack(side="left", padx=(4, 2))
    entry_busqueda = ttk.Entry(frame_filtros, width=18)
    entry_busqueda.pack(side="left", padx=(0, 10))

    ttk.Label(frame_filtros, text="Filtrar por:").pack(side="left", padx=(4, 2))
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

    btn_limpiar = ttk.Button(
        frame_filtros,
        text="Limpiar Filtros",
        command=lambda: [entry_busqueda.delete(0, tk.END), combo_filtro.current(0), cargar_datos_tabla()]
    )
    btn_limpiar.pack(side="left", padx=8)

    # ----------------------------------------------------
    # 3. Tabla Interactiva de Alumnos (ttk.Treeview)
    # ----------------------------------------------------
    frame_tabla = ttk.Frame(contenedor)
    frame_tabla.pack(fill="both", expand=True, padx=4, pady=4)

    columnas = ("dni", "nombre", "clase", "turno", "estado_cuota", "periodo", "apto", "estado")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=12)

    tabla.heading("dni", text="DNI")
    tabla.heading("nombre", text="Apellido y Nombre")
    tabla.heading("clase", text="Actividad")
    tabla.heading("turno", text="Turno")
    tabla.heading("estado_cuota", text="Estado Cuota")
    tabla.heading("periodo", text="Período")
    tabla.heading("apto", text="Apto Médico")
    tabla.heading("estado", text="Estado")

    tabla.column("dni", width=80, anchor="center")
    tabla.column("nombre", width=175, anchor="w")
    tabla.column("clase", width=95, anchor="center")
    tabla.column("turno", width=80, anchor="center")
    tabla.column("estado_cuota", width=140, anchor="center")
    tabla.column("periodo", width=90, anchor="center")
    tabla.column("apto", width=95, anchor="center")
    tabla.column("estado", width=80, anchor="center")

    scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
    tabla.configure(yscrollcommand=scroll_y.set)
    tabla.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

    def cargar_datos_tabla(event=None):
        for item in tabla.get_children():
            tabla.delete(item)

        socios = cargar_socios()
        actualizar_tarjetas(socios)

        texto = entry_busqueda.get()
        filtro = combo_filtro.get()
        socios_filtrados = filtrar_socios(texto_busqueda=texto, filtro_estado=filtro, socios=socios)

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

    combo_filtro.bind("<<ComboboxSelected>>", cargar_datos_tabla)
    entry_busqueda.bind("<KeyRelease>", cargar_datos_tabla)

    # ----------------------------------------------------
    # 4. Operaciones sobre Alumnos: Modificar y Eliminar
    # ----------------------------------------------------
    frame_gestion = ttk.Frame(contenedor, padding=4)
    frame_gestion.pack(fill="x", padx=4, pady=2)

    def obtener_socio_seleccionado():
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning(
                "Seleccionar Alumno",
                "Por favor, seleccione un alumno de la tabla haciendo un clic sobre su fila.",
                parent=ventana
            )
            return None
        item = tabla.item(seleccion[0])
        dni = str(item["values"][0]).strip()
        socios = cargar_socios()
        return buscar_socio(dni, socios)

    def modificar_alumno():
        socio = obtener_socio_seleccionado()
        if socio:
            def refrescar_todo():
                cargar_datos_tabla()
                if callback_actualizar:
                    callback_actualizar()
            pantalla_edicion.abrir(ventana, socio, callback_actualizar=refrescar_todo)

    def eliminar_alumno():
        socio = obtener_socio_seleccionado()
        if not socio:
            return

        confirmado = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Está seguro de que desea eliminar al alumno:\n\n"
            f"• Nombre: {socio.nombre} {socio.apellido}\n"
            f"• DNI: {socio.dni}\n"
            f"• Actividad: {socio.clase} (Turno: {socio.turno})\n\n"
            f"Esta acción borrará definitivamente sus registros.",
            parent=ventana
        )

        if confirmado:
            eliminar_socio(socio.dni)
            messagebox.showinfo(
                "Alumno Eliminado",
                f"El alumno {socio.nombre} {socio.apellido} fue eliminado correctamente.",
                parent=ventana
            )
            cargar_datos_tabla()
            if callback_actualizar:
                callback_actualizar()

    # Botones para modificar y eliminar
    btn_modificar = ttk.Button(frame_gestion, text="✏️ Modificar Alumno Seleccionado", command=modificar_alumno)
    btn_modificar.pack(side="left", padx=5)

    btn_eliminar = ttk.Button(frame_gestion, text="🗑️ Eliminar Alumno Seleccionado", command=eliminar_alumno)
    btn_eliminar.pack(side="left", padx=5)

    ttk.Label(
        frame_gestion,
        text="(Tip: También podés hacer doble clic sobre un alumno para modificarlo)",
        font=("Segoe UI", 8, "italic"),
        foreground="#666666"
    ).pack(side="left", padx=10)

    # Atajo: Doble clic en cualquier fila para modificar
    tabla.bind("<Double-1>", lambda event: modificar_alumno())

    cargar_datos_tabla()

    # ----------------------------------------------------
    # 5. Botones de Exportación PDF y Cierre
    # ----------------------------------------------------
    frame_acciones = ttk.Frame(contenedor, padding=6)
    frame_acciones.pack(fill="x", padx=4, pady=4)

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
        try:
            os.startfile(ruta)
        except Exception:
            pass

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
    btn_pdf_gral.pack(side="left", padx=5)

    btn_pdf_avisos = ttk.Button(frame_acciones, text="⚠️ Descargar Listado de Cobranzas y Avisos (PDF)", command=exportar_avisos)
    btn_pdf_avisos.pack(side="left", padx=5)

    btn_cerrar = ttk.Button(frame_acciones, text="Cerrar", command=ventana.destroy)
    btn_cerrar.pack(side="right", padx=5)