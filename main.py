"""
Módulo Principal - Sistema de Gestión Náutica (Kayak y Natación)
Punto de entrada de la aplicación. Configura la ventana principal,
estilos ttk, menús desplegables, accesos rápidos y tarjeta de bienvenida.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from logica import (
    cargar_socios,
    calcular_estadisticas,
    calcular_recaudacion_mes,
    generar_reporte_pdf,
    generar_reporte_avisos_pdf
)
import pantalla_clientes
import pantalla_renovacion
import pantalla_estadisticas
import pantalla_precios

# Ventana principal
root = tk.Tk()
root.title("Sistema Náutico - Gestión de Alumnos y Cuotas")
root.geometry("490x460")
root.minsize(450, 420)
root.configure(bg="#f0f4f8")

# Estilos ttk unificados (tema clam)
estilo = ttk.Style()
estilo.theme_use("clam")
estilo.configure("TButton", font=("Segoe UI", 10), padding=6)
estilo.configure("TLabel", background="#f0f4f8", font=("Segoe UI", 9))
estilo.configure("TLabelframe", background="#f0f4f8")
estilo.configure("TLabelframe.Label", background="#f0f4f8", font=("Segoe UI", 9, "bold"), foreground="#1b365d")

# ----------------------------------------------------
# Barra de Menús Desplegables (tk.Menu)
# ----------------------------------------------------
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Menú Socios
menu_socios = tk.Menu(menu_bar, tearoff=0)
menu_socios.add_command(label="Nuevo Alumno / Socio...", command=lambda: pantalla_clientes.abrir(root, actualizar_resumen))
menu_socios.add_command(label="Consultar, Modificar o Eliminar Alumnos...", command=lambda: pantalla_estadisticas.abrir(root, actualizar_resumen))
menu_bar.add_cascade(label="Alumnos", menu=menu_socios)

# Menú Cobranzas
menu_cobranzas = tk.Menu(menu_bar, tearoff=0)
menu_cobranzas.add_command(label="Registrar Cobro de Cuota...", command=lambda: pantalla_renovacion.abrir(root, actualizar_resumen))
menu_cobranzas.add_command(label="Modificar Importes de Cuotas...", command=lambda: pantalla_precios.abrir(root, actualizar_resumen))
menu_bar.add_cascade(label="Cobranzas", menu=menu_cobranzas)

# Menú Reportes
menu_reportes = tk.Menu(menu_bar, tearoff=0)
menu_reportes.add_command(label="Panel de Estadísticas y Tabla", command=lambda: pantalla_estadisticas.abrir(root, actualizar_resumen))
menu_reportes.add_separator()
menu_reportes.add_command(label="Exportar Reporte General (PDF)", command=lambda: exportar_pdf_directo("general"))
menu_reportes.add_command(label="Exportar Listado de Avisos / Cobranza (PDF)", command=lambda: exportar_pdf_directo("avisos"))
menu_bar.add_cascade(label="Reportes", menu=menu_reportes)

# Menú Sistema
def salir_programa():
    if messagebox.askyesno("Confirmar Salida", "¿Desea cerrar el sistema náutico?"):
        root.destroy()

menu_sistema = tk.Menu(menu_bar, tearoff=0)
menu_sistema.add_command(
    label="Acerca de...",
    command=lambda: messagebox.showinfo(
        "Sistema Náutico",
        "Sistema de Gestión de Alumnos y Cobranzas\n"
        "Disciplinas: Kayak y Natación (Turnos Mañana y Tarde)\n"
        "Trabajo Integrador Final - Python & Tkinter"
    )
)
menu_sistema.add_separator()
menu_sistema.add_command(label="Salir", command=salir_programa)
menu_bar.add_cascade(label="Sistema", menu=menu_sistema)


# ----------------------------------------------------
# Contenido Visual de la Ventana Principal
# ----------------------------------------------------
ttk.Label(
    root,
    text="ESCUELA NÁUTICA\nKAYAK & NATACIÓN",
    font=("Segoe UI", 15, "bold"),
    justify="center",
    foreground="#1b365d"
).pack(pady=(16, 10))

# Tarjeta de Estado y Bienvenida al Iniciar
frame_bienvenida = ttk.LabelFrame(root, text=" Estado del Club al Iniciar ", padding=10)
frame_bienvenida.pack(fill="x", padx=35, pady=6)

lbl_resumen_socios = ttk.Label(frame_bienvenida, text="", font=("Segoe UI", 9))
lbl_resumen_socios.pack(anchor="w")

lbl_resumen_ingresos = ttk.Label(frame_bienvenida, text="", font=("Segoe UI", 9, "bold"), foreground="#1b365d")
lbl_resumen_ingresos.pack(anchor="w", pady=(3, 1))

lbl_resumen_cuotas = ttk.Label(frame_bienvenida, text="", font=("Segoe UI", 9, "bold"))
lbl_resumen_cuotas.pack(anchor="w", pady=(2, 0))


def actualizar_resumen():
    """Actualiza en tiempo real los datos y métricas de la tarjeta principal."""
    socios = cargar_socios()
    stats = calcular_estadisticas(socios)
    hoy = date.today()
    periodo_actual = f"{hoy.month:02d}/{hoy.year}"
    recaudacion = calcular_recaudacion_mes(periodo=periodo_actual, socios=socios)

    lbl_resumen_socios.config(
        text=f"Fecha: {hoy.strftime('%d/%m/%Y')} | Alumnos: {stats['total']}  "
             f"(Kayak: {stats['kayak']}, Natación: {stats['natacion']}, Ambas: {stats['ambas']})"
    )

    lbl_resumen_ingresos.config(
        text=f"💵 Ingresos en cuotas ({periodo_actual}): ${recaudacion['total_recaudado']:,.2f} ({recaudacion['cantidad_pagos']} cobros)"
    )

    if hoy.day <= 10:
        texto_cuota = f"⚠️ {stats['pendientes']} alumnos pendientes de pago (Vencimiento regular: día 10)"
        color_cuota = "#9a6700"  # Ámbar
    else:
        texto_cuota = f"🚨 {stats['atrasados']} alumnos con cuota vencida (Pasó el día 10)"
        color_cuota = "#b30000"  # Rojo

    if stats["total"] > 0 and stats["al_dia"] == stats["total"]:
        texto_cuota = "✅ ¡Todos los alumnos están al día este mes!"
        color_cuota = "#197a19"

    lbl_resumen_cuotas.config(text=texto_cuota, foreground=color_cuota)


actualizar_resumen()

# ----------------------------------------------------
# Botones de Acceso Rápido
# ----------------------------------------------------
ttk.Label(root, text="Accesos Rápidos:", font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=40, pady=(12, 4))

ttk.Button(
    root,
    text="➕ Registrar Nuevo Alumno",
    command=lambda: pantalla_clientes.abrir(root, actualizar_resumen)
).pack(fill="x", padx=40, pady=3)

ttk.Button(
    root,
    text="💳 Registrar Cobro de Cuota",
    command=lambda: pantalla_renovacion.abrir(root, actualizar_resumen)
).pack(fill="x", padx=40, pady=3)

ttk.Button(
    root,
    text="💲 Modificar Importes de Cuotas",
    command=lambda: pantalla_precios.abrir(root, actualizar_resumen)
).pack(fill="x", padx=40, pady=3)

ttk.Button(
    root,
    text="📊 Consultar, Modificar Alumnos y Recaudación",
    command=lambda: pantalla_estadisticas.abrir(root, actualizar_resumen)
).pack(fill="x", padx=40, pady=3)


def exportar_pdf_directo(tipo):
    socios = cargar_socios()
    if not socios:
        messagebox.showwarning("Atención", "No hay datos de alumnos para exportar.")
        return
    if tipo == "general":
        ruta = generar_reporte_pdf(socios)
        messagebox.showinfo("Éxito", f"Reporte General guardado exitosamente en:\n{ruta}")
    else:
        ruta = generar_reporte_avisos_pdf(socios)
        messagebox.showinfo("Éxito", f"Listado de Avisos guardado exitosamente en:\n{ruta}")


root.protocol("WM_DELETE_WINDOW", salir_programa)

if __name__ == "__main__":
    root.mainloop()