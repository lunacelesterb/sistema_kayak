"""
================================================================================
ARCHIVO: main.py (Ventana Principal / Punto de Entrada del Sistema)
================================================================================

1. PROPÓSITO GENERAL:
   Es el archivo principal que inicia el programa (se ejecuta con 'python main.py').
   Su función práctica es mostrar el panel de bienvenida del Club Náutico, ofrecer
   una barra de menús desplegables arriba, mostrar un resumen automático en vivo
   (cantidad de alumnos, dinero recaudado en el mes y alertas de cuotas) y brindar
   los 4 botones grandes de acceso rápido a las demás pantallas del sistema.

2. ELEMENTOS VISUALES / INTERFAZ:
   - Ventana Principal ('root'): Mide 540x550 píxeles iniciales (mínimo 500x520).
     Tiene de fondo la imagen 'fondo.jpg' muy difuminada.
   - Barra de Menús ('menu_bar'): Ubicada en el borde superior con 4 pestañas
     desplegables: "Alumnos", "Cobranzas", "Reportes" y "Sistema" (fuente Roboto 9).
   - Botón Conmutador de Tema (☀️ / 🌙): Ubicado arriba a la derecha para alternar
     entre Modo Día (claro) y Modo Noche (oscuro) en tiempo real.
   - Título Principal: Etiqueta centrada "ESCUELA NÁUTICA / KAYAK & NATACIÓN" en
     fuente Roboto tamaño 15 en negrita ("bold") y color azul.
   - Tarjeta de Resumen ('frame_bienvenida'): Un cuadro blanco (o azul oscuro en
     Modo Noche) con borde Azul Glicina (#779be7) que muestra 3 renglones dinámicos:
     1) Fecha actual y total de alumnos por deporte.
     2) Total de dinero recaudado en el mes actual.
     3) Alerta de cuotas pendientes/vencidas con colores tipo semáforo.
   - 4 Botones de Acceso Rápido ('ttk.Button'): Ocupan todo el ancho disponible,
     cambian a color Cielo Fresco (#49b6ff) con letra blanca al pasar el mouse
     (efecto Hover) y agrandan su letra al hacer clic.

3. EXPLICACIÓN LÍNEA POR LÍNEA:
   Cada bloque e instrucción está explicado en los comentarios debajo.
================================================================================
"""

# Aquí importamos 'tkinter' (como 'tk') para crear la ventana principal y la barra de menús
import tkinter as tk
# Aquí importamos 'ttk' (componentes gráficos modernos) y 'messagebox' (carteles emergentes de aviso)
from tkinter import ttk, messagebox
# Aquí importamos 'date' para saber qué día es hoy y mostrarlo en el resumen inicial
from datetime import date

# Aquí importamos las funciones de lógica y diseño visual que programamos en 'logica.py'
from logica import (
    cargar_socios,               # Lee la lista de alumnos desde 'clientes.json'
    calcular_estadisticas,       # Cuenta cuántos alumnos hay en Kayak, Natación, turnos, etc.
    calcular_recaudacion_mes,    # Suma el dinero cobrado en el mes actual
    generar_reporte_pdf,         # Crea el archivo PDF con el padrón completo de socios
    generar_reporte_avisos_pdf,  # Crea el archivo PDF solo con los socios que adeudan el mes
    configurar_estilos_modernos, # Aplica los colores, fuentes, imagen difuminada y efectos de botones
    crear_boton_tema,            # Crea el botón 🌙 / ☀️ arriba a la derecha
    obtener_tema_actual,         # Consulta si estamos en Modo Día o en Modo Noche
    FUENTE_PRINCIPAL             # Nombre de la fuente tipográfica principal ("Roboto")
)

# Aquí importamos los otros 4 archivos de pantallas para poder abrirlos cuando el usuario haga clic
import pantalla_clientes
import pantalla_renovacion
import pantalla_estadisticas
import pantalla_precios

# ----------------------------------------------------
# Creación y Tamaño de la Ventana Principal
# ----------------------------------------------------
# Aquí se crea la ventana principal del programa (llamada 'root' o raíz)
root = tk.Tk()
# Aquí se define el título que aparece en la barra superior de la ventana en Windows
root.title("Sistema Náutico - Gestión de Alumnos y Cuotas")
# Aquí se define el tamaño inicial de la ventana: 540 píxeles de ancho por 550 píxeles de alto
root.geometry("540x550")
# Aquí se define el tamaño mínimo al achicar la ventana para que nunca se tapen los botones
root.minsize(500, 520)

# Aquí se aplica la imagen de fondo difuminada, la paleta de tonos azules y los efectos de botones.
# Además, 'callback_tema' indica que si el usuario cambia entre Día y Noche, se refresque el resumen.
estilo = configurar_estilos_modernos(root, callback_tema=lambda _tema: actualizar_resumen())

# ----------------------------------------------------
# Barra de Menús Desplegables Superior (tk.Menu)
# ----------------------------------------------------
# Aquí se crea la barra horizontal de menús con la fuente de letra Roboto tamaño 9
menu_bar = tk.Menu(root, font=(FUENTE_PRINCIPAL, 9))
# Aquí le indicamos a la ventana principal que utilice esta barra de menús
root.config(menu=menu_bar)

# 1. Menú desplegable "Alumnos" (tearoff=0 evita que el menú se pueda desprender como ventana suelta)
menu_socios = tk.Menu(menu_bar, tearoff=0, font=(FUENTE_PRINCIPAL, 9))
# Aquí se maneja lo que pasa al hacer clic en "Nuevo Alumno": abre 'pantalla_clientes'
menu_socios.add_command(label="Nuevo Alumno / Socio...", command=lambda: pantalla_clientes.abrir(root, actualizar_resumen))
# Aquí se maneja lo que pasa al hacer clic en "Consultar, Modificar o Eliminar": abre 'pantalla_estadisticas'
menu_socios.add_command(label="Consultar, Modificar o Eliminar Alumnos...", command=lambda: pantalla_estadisticas.abrir(root, actualizar_resumen))
# Agregamos la pestaña "Alumnos" a la barra superior
menu_bar.add_cascade(label="Alumnos", menu=menu_socios)

# 2. Menú desplegable "Cobranzas"
menu_cobranzas = tk.Menu(menu_bar, tearoff=0, font=(FUENTE_PRINCIPAL, 9))
# Abre la pantalla para cobrar una cuota mensual
menu_cobranzas.add_command(label="Registrar Cobro de Cuota...", command=lambda: pantalla_renovacion.abrir(root, actualizar_resumen))
# Abre la pantalla para cambiar los precios de Kayak, Natación y Ambas
menu_cobranzas.add_command(label="Modificar Importes de Cuotas...", command=lambda: pantalla_precios.abrir(root, actualizar_resumen))
menu_bar.add_cascade(label="Cobranzas", menu=menu_cobranzas)

# 3. Menú desplegable "Reportes"
menu_reportes = tk.Menu(menu_bar, tearoff=0, font=(FUENTE_PRINCIPAL, 9))
menu_reportes.add_command(label="Panel de Estadísticas y Tabla", command=lambda: pantalla_estadisticas.abrir(root, actualizar_resumen))
# Dibuja una línea horizontal divisoria dentro del menú
menu_reportes.add_separator()
# Permite exportar directamente el PDF general o el de avisos de cobro desde el menú
menu_reportes.add_command(label="Exportar Reporte General (PDF)", command=lambda: exportar_pdf_directo("general"))
menu_reportes.add_command(label="Exportar Listado de Avisos / Cobranza (PDF)", command=lambda: exportar_pdf_directo("avisos"))
menu_bar.add_cascade(label="Reportes", menu=menu_reportes)


# Aquí se define la función para confirmar si el usuario realmente quiere salir del sistema
def salir_programa():
    # Muestra un cartel con botones "Sí" y "No"; si elige "Sí" (True), cierra la ventana principal
    if messagebox.askyesno("Confirmar Salida", "¿Desea cerrar el sistema náutico?"):
        root.destroy()


# 4. Menú desplegable "Sistema"
menu_sistema = tk.Menu(menu_bar, tearoff=0, font=(FUENTE_PRINCIPAL, 9))
# Muestra una ventana informativa con los créditos del Trabajo Integrador Final
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
# Botón Conmutador de Tema (🌙 Modo Noche / ☀️ Modo Día)
# ----------------------------------------------------
# Aquí se coloca arriba a la derecha (anchor="ne") el botón para alternar entre Modo Claro y Oscuro
crear_boton_tema(root, padx=35, pady=(10, 0))

# ----------------------------------------------------
# Título y Tarjeta de Resumen del Club (Dashboard)
# ----------------------------------------------------
# Aquí se crea el título grande central usando el estilo "Header.TLabel" (Roboto 15 en negrita)
ttk.Label(
    root,
    text="ESCUELA NÁUTICA\nKAYAK & NATACIÓN",
    style="Header.TLabel",
    justify="center"
).pack(pady=(4, 10))

# Aquí se crea la tarjeta con marco ("LabelFrame") donde se muestra el resumen del club al iniciar.
# 'padding=12' deja un margen interno de 12 píxeles y 'fill="x"' hace que se estire horizontalmente.
frame_bienvenida = ttk.LabelFrame(root, text=" ✨ Estado del Club al Iniciar ", padding=12)
frame_bienvenida.pack(fill="x", padx=35, pady=6)

# Etiqueta 1 de la tarjeta: mostrará la fecha y la cantidad de socios (alineada a la izquierda: anchor="w")
lbl_resumen_socios = ttk.Label(frame_bienvenida, text="", style="Card.TLabel")
lbl_resumen_socios.pack(anchor="w")

# Etiqueta 2 de la tarjeta: mostrará el dinero recaudado en el mes en color azul destacado
lbl_resumen_ingresos = ttk.Label(
    frame_bienvenida,
    text="",
    style="Accent.Card.TLabel"
)
lbl_resumen_ingresos.pack(anchor="w", pady=(4, 2))

# Etiqueta 3 de la tarjeta: mostrará la situación de cuotas con fuente Roboto 9 en negrita ("bold")
lbl_resumen_cuotas = ttk.Label(frame_bienvenida, text="", style="Card.TLabel", font=(FUENTE_PRINCIPAL, 9, "bold"))
lbl_resumen_cuotas.pack(anchor="w", pady=(2, 0))


def actualizar_resumen():
    """
    Aquí se actualiza en tiempo real el texto y el color de las 3 etiquetas de la tarjeta principal.
    Esta función se ejecuta al abrir el programa y cada vez que se agrega, edita, elimina o cobra a un socio.
    """
    # 1. Cargamos la lista actualizada de socios desde 'clientes.json'
    socios = cargar_socios()
    # 2. Calculamos las cantidades totales (cuántos hacen Kayak, Natación, Ambas, al día, atrasados)
    stats = calcular_estadisticas(socios)
    # 3. Obtenemos la fecha de hoy y armamos el período actual (ejemplo: "10/2026")
    hoy = date.today()
    periodo_actual = f"{hoy.month:02d}/{hoy.year}"
    # 4. Calculamos cuánto dinero ingresó en este mes y cuántos cobros se registraron
    recaudacion = calcular_recaudacion_mes(periodo=periodo_actual, socios=socios)
    # 5. Consultamos si la interfaz está en Modo Día o en Modo Noche para elegir el tono más legible
    tema = obtener_tema_actual()
    es_noche = tema["nombre"] == "nocturno"

    # Actualizamos el texto del primer renglón con la fecha y el conteo de alumnos
    lbl_resumen_socios.config(
        text=f"Fecha: {hoy.strftime('%d/%m/%Y')} | Alumnos: {stats['total']}  "
             f"(Kayak: {stats['kayak']}, Natación: {stats['natacion']}, Ambas: {stats['ambas']})"
    )

    # Actualizamos el segundo renglón con el monto recaudado formateado con separador de miles y 2 decimales
    lbl_resumen_ingresos.config(
        text=f"💵 Ingresos en cuotas ({periodo_actual}): ${recaudacion['total_recaudado']:,.2f} ({recaudacion['cantidad_pagos']} cobros)"
    )

    # Aquí se define el color y el mensaje de alerta según el día del mes:
    if hoy.day <= 10:
        # Del día 1 al 10 del mes: recordatorio preventivo en tono ámbar/dorado
        texto_cuota = f"⚠️ {stats['pendientes']} alumnos pendientes de pago (Vencimiento regular: día 10)"
        color_cuota = "#fbbf24" if es_noche else "#b45309"
    else:
        # Después del día 10: alerta de cuotas vencidas en tono rosa intenso / carmesí
        texto_cuota = f"🚨 {stats['atrasados']} alumnos con cuota vencida (Pasó el día 10)"
        color_cuota = "#ff499e" if es_noche else "#be123c"

    # Si todos los alumnos registrados ya pagaron este mes, mostramos un mensaje de felicitación
    if stats["total"] > 0 and stats["al_dia"] == stats["total"]:
        texto_cuota = "✅ ¡Todos los alumnos están al día este mes!"
        color_cuota = "#49b6ff" if es_noche else "#15803d"

    # Aplicamos el texto y el color elegido a la tercera etiqueta
    lbl_resumen_cuotas.config(text=texto_cuota, foreground=color_cuota)


# Llamamos a la función por primera vez al arrancar el programa para que la tarjeta aparezca completa
actualizar_resumen()

# ----------------------------------------------------
# Botones de Acceso Rápido (con Efecto Hover y Clic)
# ----------------------------------------------------
# Subtítulo encima de la botonera
ttk.Label(
    root,
    text="Accesos Rápidos del Panel:",
    style="SubHeader.TLabel"
).pack(anchor="w", padx=35, pady=(12, 4))

# Botón 1: Al hacer clic abre la ventana para dar de alta un nuevo alumno ('pantalla_clientes.py')
ttk.Button(
    root,
    text="➕ Registrar Nuevo Alumno",
    command=lambda: pantalla_clientes.abrir(root, actualizar_resumen)
).pack(fill="x", padx=35, pady=4)

# Botón 2: Al hacer clic abre la ventana de cobro de cuotas y búsqueda de homónimos ('pantalla_renovacion.py')
ttk.Button(
    root,
    text="💳 Registrar Cobro de Cuota",
    command=lambda: pantalla_renovacion.abrir(root, actualizar_resumen)
).pack(fill="x", padx=35, pady=4)

# Botón 3: Al hacer clic abre la ventana para cambiar el valor de las cuotas ('pantalla_precios.py')
ttk.Button(
    root,
    text="💲 Modificar Importes de Cuotas",
    command=lambda: pantalla_precios.abrir(root, actualizar_resumen)
).pack(fill="x", padx=35, pady=4)

# Botón 4: Al hacer clic abre el panel con la tabla completa, filtros, edición y PDFs ('pantalla_estadisticas.py')
ttk.Button(
    root,
    text="📊 Consultar, Modificar Alumnos y Recaudación",
    command=lambda: pantalla_estadisticas.abrir(root, actualizar_resumen)
).pack(fill="x", padx=35, pady=4)


# Función auxiliar para exportar los PDFs cuando se eligen desde el menú superior "Reportes"
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


# Aquí interceptamos el clic en la "X" de cerrar ventana para pedir confirmación antes de salir
root.protocol("WM_DELETE_WINDOW", salir_programa)

# Aquí se inicia el bucle principal de eventos ('mainloop') que mantiene la ventana abierta en pantalla
if __name__ == "__main__":
    root.mainloop()
