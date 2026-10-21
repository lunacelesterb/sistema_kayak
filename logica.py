"""
================================================================================
ARCHIVO: logica.py (Motor Visual, Búsquedas, Persistencia JSON y Reportes PDF)
================================================================================

1. PROPÓSITO GENERAL:
   Es el módulo central de servicios del sistema. Cumple dos grandes funciones:
   A) MOTOR VISUAL E INTERACTIVO: Carga y difumina la imagen 'fondo.jpg' con Pillow,
      define la paleta de colores (priorizando azules #779be7 y #49b6ff con leves
      detalles en rosa pétalo #d264b6), controla el botón para alternar entre
      Modo Día (☀️) y Modo Noche (🌙) en todas las ventanas a la vez, y configura
      los efectos de los botones (inversión de color al pasar el cursor y aumento
      del tamaño de la letra al hacer clic).
   B) LÓGICA DE NEGOCIO, JSON Y PDF: Lee y guarda 'clientes.json', busca socios
      por DNI o Nombre (incluyendo la búsqueda múltiple de homónimos), elimina o
      edita registros, calcula las estadísticas y la recaudación mensual, y genera
      los 2 reportes en formato PDF con la librería 'fpdf2'.

2. ELEMENTOS VISUALES / INTERFAZ QUE CONTROLA:
   - Fuente de la letra: Define 'FUENTE_PRINCIPAL = "Roboto"' y 'FUENTE_ALTERNATIVA = "Segoe UI"'
     (evitando Arial).
   - Paleta de colores ('TEMAS["claro"]' y 'TEMAS["nocturno"]'):
     * Azul Glicina (#779be7): Marcos de tarjetas, bordes de campos de entrada,
       encabezados de tablas y fondo de botón al hacer clic.
     * Cielo Fresco (#49b6ff): Fondo de botón al pasar el cursor (Hover), fila
       seleccionada en tablas y títulos en Modo Nocturno.
     * Rosa Pétalo (#d264b6) y Fruta del Dragón (#ff499e): Acentos muy leves y
       puntuales en el borde del botón de tema y en el borde activo al interactuar.
   - Imagen de fondo ('_lbl_fondo'): Etiqueta posicionada con '.place(relwidth=1, relheight=1)'
     en el fondo de cada ventana con 'fondo.jpg' desenfocada (GaussianBlur radio 14)
     y baja opacidad (24% en Modo Día y 20% en Modo Noche).
   - Botones ('TButton' y 'Pressed.TButton'): Padding (12, 7), borde de 2px, fuente
     Roboto 10 negrita que crece a tamaño 11 negrita cuando el usuario hace clic.

3. EXPLICACIÓN LÍNEA POR LÍNEA:
   Cada bloque e instrucción está explicado en lenguaje llano debajo.
================================================================================
"""

# Aquí importamos 'json' para leer/escribir 'clientes.json' y 'os' para manejar rutas de archivos
import json
import os
# Aquí importamos 'datetime' y 'date' para consultar la fecha y hora actual en cálculos y PDFs
from datetime import datetime, date
# Aquí importamos 'tkinter' y 'ttk' para configurar los estilos visuales de las ventanas
import tkinter as tk
from tkinter import ttk
# Aquí importamos 'FPDF' (de la librería 'fpdf2') para construir los documentos PDF
from fpdf import FPDF
# Aquí importamos la clase 'Socio' y las funciones de precios desde nuestro archivo 'datos.py'
from datos import Socio, cargar_precios, guardar_precios

# Aquí importamos Pillow ('PIL') para abrir la imagen 'fondo.jpg', difuminarla y mostrarla en Tkinter.
# Se envuelve en 'try...except' para que, si en alguna PC no estuviera instalado Pillow, el programa
# funcione igual con fondo de color liso sin dar error.
try:
    from PIL import Image, ImageTk, ImageFilter
    PILLOW_DISPONIBLE = True
except ImportError:
    PILLOW_DISPONIBLE = False

# ----------------------------------------------------
# Configuración de Rutas de Archivos del Proyecto
# ----------------------------------------------------
# Carpeta exacta donde se encuentra este script
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
# Ruta hacia la base de datos de alumnos ('clientes.json')
RUTA_JSON = os.path.join(DIRECTORIO_ACTUAL, "clientes.json")
# Rutas donde se guardarán los dos reportes en formato PDF
RUTA_PDF_GENERAL = os.path.join(DIRECTORIO_ACTUAL, "reporte_socios.pdf")
RUTA_PDF_AVISOS = os.path.join(DIRECTORIO_ACTUAL, "reporte_avisos_cobro.pdf")
# Ruta hacia la imagen de fondo guardada en la carpeta del proyecto
RUTA_IMAGEN_FONDO = os.path.join(DIRECTORIO_ACTUAL, "fondo.jpg")

# ----------------------------------------------------
# Aquí se definen los colores y la fuente de la letra
# ----------------------------------------------------
COLOR_AZUL_GLICINA = "#779be7"    # Azul glicina (Base principal para marcos, cabeceras y títulos)
COLOR_CIELO_FRESCO = "#49b6ff"    # Cielo fresco (Base principal para destaques, hover y títulos)
COLOR_AZUL_PROFUNDO = "#2b5cb8"   # Azul intenso para óptima legibilidad en modo claro
COLOR_LAVANDA = "#a480cf"         # Lavanda brillante (Transición suave)
COLOR_ROSA_PETALO = "#d264b6"     # Rosa Pétalo (Acento sutil y puntual en bordes activos)
COLOR_FRUTA_DRAGON = "#ff499e"    # Fruta del Dragón (Detalle puntual mínimo)

# Constantes generales y tipografías limpias (priorizando Roboto y Segoe UI, evitando Arial)
COLOR_FONDO_APP = "#f2f7fd"
COLOR_TARJETA = "#ffffff"
COLOR_AZUL_CORP = COLOR_AZUL_GLICINA
COLOR_AZUL_VIBRANTE = COLOR_CIELO_FRESCO
COLOR_AZUL_PRESIONADO = COLOR_AZUL_GLICINA
FUENTE_PRINCIPAL = "Roboto"
FUENTE_ALTERNATIVA = "Segoe UI"

# Aquí se definen las dos paletas completas del sistema: Modo Día ("claro") y Modo Noche ("nocturno")
TEMAS = {
    "claro": {
        "nombre": "claro",
        "fondo_app": "#f2f7fd",           # Blanco celeste náutico muy suave
        "fondo_blend": (242, 247, 253),   # Color RGB con el que se funde 'fondo.jpg' en Modo Día
        "opacidad_img": 0.24,             # Opacidad baja (24%) para que la foto de fondo no sature la vista
        "tarjeta": "#ffffff",             # Blanco puro para el interior de las tarjetas
        "texto": "#1e293b",               # Azul pizarra oscuro muy legible para textos generales
        "texto_secundario": "#5b708b",    # Gris azulado para textos aclaratorios
        "titulo_principal": "#2b5cb8",    # Azul profundo para el título principal
        "titulo_card": "#779be7",         # Azul glicina para los títulos de las tarjetas
        "borde_card": "#779be7",          # Azul glicina para los bordes de las tarjetas
        "btn_bg": "#ffffff",              # Fondo blanco en botones en estado normal
        "btn_fg": "#2b5cb8",              # Letra azul en botones en estado normal
        "btn_borde": "#779be7",           # Borde Azul glicina en botones normales
        "btn_hover_bg": "#49b6ff",        # Fondo Cielo fresco (#49b6ff) cuando pasa el mouse por encima
        "btn_hover_fg": "#ffffff",        # Letra blanca cuando pasa el mouse por encima
        "btn_press_bg": "#779be7",        # Fondo Azul glicina cuando se hace clic en el botón
        "acento_sutil": "#d264b6",        # Detalle leve en Rosa Pétalo (#d264b6) solo en bordes puntuales
        "entry_bg": "#ffffff",
        "entry_fg": "#1e293b",
        "entry_borde": "#779be7",
        "tree_bg": "#ffffff",
        "tree_fg": "#1e293b",
        "tree_head_bg": "#779be7",        # Encabezado de tabla en Azul glicina
        "tree_head_fg": "#ffffff",
        "tree_head_active": "#49b6ff",    # Encabezado en Cielo fresco al pasar el cursor
        "tree_sel_bg": "#49b6ff",         # Fila seleccionada de la tabla en Cielo fresco
        "listbox_bg": "#f4f8fe",
        "listbox_fg": "#1e293b",
        "apoyo_glicina": "#779be7",
        "apoyo_cielo": "#49b6ff",
        "texto_toggle": "🌙 Modo Noche"
    },
    "nocturno": {
        "nombre": "nocturno",
        "fondo_app": "#0f172a",           # Azul noche profundo para el fondo general
        "fondo_blend": (15, 23, 42),      # Color RGB oscuro con el que se funde 'fondo.jpg' en Modo Noche
        "opacidad_img": 0.20,             # Opacidad suave nocturna (20%)
        "tarjeta": "#1e293b",             # Gris/azul pizarra oscuro elegante para tarjetas
        "texto": "#f1f5f9",               # Texto blanco hielo muy legible sobre fondo oscuro
        "texto_secundario": "#94a3b8",    # Gris celeste claro para textos secundarios
        "titulo_principal": "#49b6ff",    # Cielo fresco luminoso para títulos
        "titulo_card": "#49b6ff",         # Cielo fresco para títulos de tarjetas
        "borde_card": "#779be7",          # Azul glicina para bordes de tarjetas
        "btn_bg": "#26354d",              # Fondo azul oscuro elegante para botones en reposo
        "btn_fg": "#49b6ff",              # Texto Cielo fresco en botones en reposo
        "btn_borde": "#779be7",           # Borde Azul glicina
        "btn_hover_bg": "#49b6ff",        # Al pasar el cursor (Hover): Cielo fresco vibrante (#49b6ff)
        "btn_hover_fg": "#ffffff",        # Letra blanca en Hover
        "btn_press_bg": "#779be7",        # Al hacer clic: Azul glicina (#779be7)
        "acento_sutil": "#d264b6",        # Detalle rosa pétalo leve en el borde activo
        "entry_bg": "#26354d",
        "entry_fg": "#ffffff",
        "entry_borde": "#779be7",
        "tree_bg": "#1e293b",
        "tree_fg": "#f1f5f9",
        "tree_head_bg": "#779be7",
        "tree_head_fg": "#ffffff",
        "tree_head_active": "#49b6ff",
        "tree_sel_bg": "#49b6ff",
        "listbox_bg": "#26354d",
        "listbox_fg": "#f1f5f9",
        "apoyo_glicina": "#779be7",
        "apoyo_cielo": "#49b6ff",
        "texto_toggle": "☀️ Modo Día"
    }
}

# Variables globales que recuerdan en qué modo estamos ("claro" o "nocturno"),
# guardan la imagen difuminada en memoria (_CACHE_IMG_BASE) y listan las ventanas abiertas
_MODO_ACTUAL = "claro"
_CACHE_IMG_BASE = {}
_VENTANAS_REGISTRADAS = []


def obtener_tema_actual():
    """Devuelve el diccionario de colores correspondiente al tema activo ('claro' o 'nocturno')."""
    return TEMAS[_MODO_ACTUAL]


def _preparar_imagenes_base():
    """
    Aquí se abre la imagen 'fondo.jpg' con Pillow, se le aplica un desenfoque Gaussiano
    fuerte (radio 14) y se mezcla con baja opacidad sobre el color de fondo del Modo Día
    y del Modo Noche para que sea suave y permita leer perfectamente los textos.
    """
    if not PILLOW_DISPONIBLE or _CACHE_IMG_BASE:
        return

    if not os.path.exists(RUTA_IMAGEN_FONDO):
        return

    try:
        # 1. Abrimos 'fondo.jpg' en modo de color RGB
        img_original = Image.open(RUTA_IMAGEN_FONDO).convert("RGB")
        resample_mode = getattr(Image, "Resampling", Image).LANCZOS
        img_redim = img_original.resize((1000, 750), resample_mode)

        # 2. Aplicamos el filtro GaussianBlur(radius=14) para difuminar la imagen
        img_difuminada = img_redim.filter(ImageFilter.GaussianBlur(radius=14))

        # 3. Preparamos una versión suave para Modo Día y otra para Modo Noche usando Image.blend()
        for clave, cfg in TEMAS.items():
            capa_color = Image.new("RGB", img_difuminada.size, cfg["fondo_blend"])
            _CACHE_IMG_BASE[clave] = Image.blend(capa_color, img_difuminada, alpha=cfg["opacidad_img"])
    except Exception:
        pass


def _actualizar_fondo_ventana(ventana, ancho=None, alto=None):
    """
    Ajusta la imagen de fondo difuminada al tamaño actual de la ventana utilizando ImageTk.PhotoImage.
    """
    if not ventana.winfo_exists():
        return

    tema = obtener_tema_actual()
    ventana.configure(bg=tema["fondo_app"])

    lbl_fondo = getattr(ventana, "_lbl_fondo", None)
    if lbl_fondo is None or not lbl_fondo.winfo_exists():
        return

    lbl_fondo.configure(bg=tema["fondo_app"])

    _preparar_imagenes_base()
    img_base = _CACHE_IMG_BASE.get(_MODO_ACTUAL)
    if img_base is None:
        return

    try:
        # Tomamos el ancho y alto actual de la ventana y redimensionamos la imagen difuminada
        w = max(ancho or ventana.winfo_width(), 300)
        h = max(alto or ventana.winfo_height(), 250)
        resample_mode = getattr(Image, "Resampling", Image).BILINEAR
        img_ajustada = img_base.resize((w, h), resample_mode)
        # Convertimos la imagen de Pillow a un objeto PhotoImage compatible con Tkinter
        foto_tk = ImageTk.PhotoImage(img_ajustada, master=ventana)
        # Guardamos una referencia en 'ventana._img_fondo_tk' para que Python no borre la imagen de la memoria
        ventana._img_fondo_tk = foto_tk
        lbl_fondo.configure(image=foto_tk)
        # '.lower()' envía la imagen detrás de todas las tarjetas, textos y botones
        lbl_fondo.lower()
    except Exception:
        pass


def _aplicar_estilos_ttk(ventana):
    """
    Aquí se configuran los colores, las fuentes de letra y los estilos de todos los
    elementos gráficos (tarjetas, textos, cajas de entrada, tablas y botones).
    """
    tema = obtener_tema_actual()
    estilo = ttk.Style(ventana)
    # Usamos el tema base 'clam' porque permite personalizar todos los colores en cualquier sistema operativo
    estilo.theme_use("clam")

    # Aquí se configura el color de fondo de los contenedores (Frames)
    estilo.configure("TFrame", background=tema["fondo_app"])
    estilo.configure("Card.TFrame", background=tema["tarjeta"])

    # Aquí se define la fuente de la letra y los colores de las etiquetas de texto (Labels)
    estilo.configure(
        "TLabel",
        background=tema["fondo_app"],
        foreground=tema["texto"],
        font=(FUENTE_PRINCIPAL, 9)
    )
    estilo.configure(
        "Card.TLabel",
        background=tema["tarjeta"],
        foreground=tema["texto"],
        font=(FUENTE_PRINCIPAL, 9)
    )
    estilo.configure(
        "Header.TLabel",
        background=tema["fondo_app"],
        foreground=tema["titulo_principal"],
        font=(FUENTE_PRINCIPAL, 15, "bold")
    )
    estilo.configure(
        "SubHeader.TLabel",
        background=tema["fondo_app"],
        foreground=tema["titulo_card"],
        font=(FUENTE_PRINCIPAL, 10, "bold")
    )
    estilo.configure(
        "Muted.Card.TLabel",
        background=tema["tarjeta"],
        foreground=tema["texto_secundario"],
        font=(FUENTE_PRINCIPAL, 8, "italic")
    )
    estilo.configure(
        "Accent.Card.TLabel",
        background=tema["tarjeta"],
        foreground=tema["titulo_principal"],
        font=(FUENTE_PRINCIPAL, 9, "bold")
    )

    # Aquí se configura el estilo de las tarjetas con marco (ttk.LabelFrame) en Azul Glicina (#779be7)
    estilo.configure(
        "TLabelframe",
        background=tema["tarjeta"],
        bordercolor=tema["borde_card"],
        lightcolor=tema["borde_card"],
        darkcolor=tema["borde_card"],
        borderwidth=2,
        relief="solid"
    )
    estilo.configure(
        "TLabelframe.Label",
        background=tema["tarjeta"],
        foreground=tema["titulo_card"],
        font=(FUENTE_PRINCIPAL, 10, "bold")
    )

    # Aquí se configuran las cajas de texto (TEntry) y listas desplegables (TCombobox)
    estilo.configure(
        "TEntry",
        fieldbackground=tema["entry_bg"],
        foreground=tema["entry_fg"],
        insertcolor=tema["entry_fg"],
        bordercolor=tema["entry_borde"],
        lightcolor=tema["entry_borde"],
        darkcolor=tema["entry_borde"],
        padding=4,
        font=(FUENTE_PRINCIPAL, 9)
    )
    estilo.configure(
        "TCombobox",
        fieldbackground=tema["entry_bg"],
        background=tema["btn_bg"],
        foreground=tema["entry_fg"],
        arrowcolor=tema["titulo_principal"],
        bordercolor=tema["entry_borde"],
        padding=4,
        font=(FUENTE_PRINCIPAL, 9)
    )
    estilo.map(
        "TCombobox",
        fieldbackground=[("readonly", tema["entry_bg"])],
        foreground=[("readonly", tema["entry_fg"])],
        selectbackground=[("readonly", tema["btn_hover_bg"])],
        selectforeground=[("readonly", "#ffffff")]
    )

    # Aquí se configura la tabla de socios (Treeview) y sus encabezados de columna
    estilo.configure(
        "Treeview",
        background=tema["tree_bg"],
        fieldbackground=tema["tree_bg"],
        foreground=tema["tree_fg"],
        bordercolor=tema["borde_card"],
        rowheight=26,
        font=(FUENTE_PRINCIPAL, 9)
    )
    estilo.configure(
        "Treeview.Heading",
        background=tema["tree_head_bg"],
        foreground=tema["tree_head_fg"],
        font=(FUENTE_PRINCIPAL, 9, "bold"),
        padding=5
    )
    estilo.map(
        "Treeview",
        background=[("selected", tema["tree_sel_bg"])],
        foreground=[("selected", "#ffffff")]
    )
    estilo.map(
        "Treeview.Heading",
        background=[("active", tema["tree_head_active"])]
    )

    # -------------------------------------------------------------------------
    # Aquí se configura el color, el tamaño y los efectos del botón (TButton)
    # -------------------------------------------------------------------------
    # Aspecto normal del botón: fuente Roboto 10 en negrita, borde de 2 píxeles y relleno (12, 7)
    estilo.configure(
        "TButton",
        font=(FUENTE_PRINCIPAL, 10, "bold"),
        background=tema["btn_bg"],
        foreground=tema["btn_fg"],
        bordercolor=tema["btn_borde"],
        lightcolor=tema["btn_bg"],
        darkcolor=tema["borde_card"],
        borderwidth=2,
        padding=(12, 7)
    )
    # 'estilo.map' controla los efectos dinámicos al pasar el cursor ("active") o hacer clic ("pressed"):
    estilo.map(
        "TButton",
        background=[
            ("pressed", tema["btn_press_bg"]),   # Al hacer clic: fondo Azul glicina (#779be7)
            ("active", tema["btn_hover_bg"]),    # Efecto Hover (pasar el mouse): fondo Cielo fresco (#49b6ff)
            ("!disabled", tema["btn_bg"])        # En reposo: blanco (Modo Día) o azul oscuro (Modo Noche)
        ],
        foreground=[
            ("pressed", "#ffffff"),              # Al hacer clic: letra blanca
            ("active", tema["btn_hover_fg"]),    # Efecto Hover: letra blanca
            ("!disabled", tema["btn_fg"])        # En reposo: letra azul
        ],
        font=[
            ("pressed", (FUENTE_PRINCIPAL, 11, "bold")), # Al hacer clic: la letra crece a tamaño 11
            ("active", (FUENTE_PRINCIPAL, 10, "bold"))
        ],
        bordercolor=[
            ("pressed", COLOR_FRUTA_DRAGON),     # Sutil borde rosa al hacer clic
            ("active", tema["acento_sutil"]),    # Sutil borde Rosa Pétalo (#d264b6) al pasar el mouse
            ("!disabled", tema["btn_borde"])     # Borde Azul glicina en reposo
        ],
        relief=[
            ("pressed", "sunken"),
            ("!pressed", "raised")
        ]
    )

    # Estilo especial 'Pressed.TButton' que fuerza el crecimiento de la letra a tamaño 11 al presionar el botón
    estilo.configure(
        "Pressed.TButton",
        font=(FUENTE_PRINCIPAL, 11, "bold"),
        background=tema["btn_press_bg"],
        foreground="#ffffff",
        bordercolor=COLOR_FRUTA_DRAGON,
        borderwidth=2,
        padding=(12, 7)
    )
    estilo.map(
        "Pressed.TButton",
        background=[("active", tema["btn_press_bg"]), ("!disabled", tema["btn_press_bg"])],
        foreground=[("active", "#ffffff"), ("!disabled", "#ffffff")]
    )

    # Aquí se configura el estilo del botón conmutador de tema (🌙 Modo Noche / ☀️ Modo Día)
    estilo.configure(
        "Theme.TButton",
        font=(FUENTE_PRINCIPAL, 9, "bold"),
        background=tema["btn_bg"],
        foreground=tema["btn_fg"],
        bordercolor=tema["acento_sutil"],
        borderwidth=2,
        padding=(10, 4)
    )
    estilo.map(
        "Theme.TButton",
        background=[
            ("pressed", tema["btn_press_bg"]),
            ("active", tema["btn_hover_bg"]),
            ("!disabled", tema["btn_bg"])
        ],
        foreground=[
            ("pressed", "#ffffff"),
            ("active", "#ffffff"),
            ("!disabled", tema["btn_fg"])
        ],
        bordercolor=[
            ("pressed", COLOR_FRUTA_DRAGON),
            ("active", tema["apoyo_cielo"]),
            ("!disabled", tema["acento_sutil"])
        ],
        font=[
            ("pressed", (FUENTE_PRINCIPAL, 10, "bold")),
            ("active", (FUENTE_PRINCIPAL, 9, "bold"))
        ]
    )

    return estilo


def alternar_tema():
    """
    Aquí se maneja lo que pasa cuando el usuario hace clic en el botón 🌙 / ☀️:
    Cambia instantáneamente toda la aplicación entre Modo Día y Modo Noche,
    actualizando colores, fondos difuminados y textos en todas las ventanas abiertas.
    """
    global _MODO_ACTUAL, COLOR_FONDO_APP, COLOR_TARJETA
    # Invertimos el modo actual: si era 'claro' pasa a 'nocturno', y viceversa
    _MODO_ACTUAL = "nocturno" if _MODO_ACTUAL == "claro" else "claro"
    tema = obtener_tema_actual()
    COLOR_FONDO_APP = tema["fondo_app"]
    COLOR_TARJETA = tema["tarjeta"]

    ventanas_vivas = []
    # Recorremos todas las ventanas abiertas para actualizarles los estilos y la imagen de fondo
    for reg in _VENTANAS_REGISTRADAS:
        ventana = reg["ventana"]
        callback = reg.get("callback")
        if ventana.winfo_exists():
            ventanas_vivas.append(reg)
            _aplicar_estilos_ttk(ventana)
            _actualizar_fondo_ventana(ventana)

            # Cambiamos el texto del botón entre "🌙 Modo Noche" y "☀️ Modo Día"
            btn_tema = getattr(ventana, "_btn_tema", None)
            if btn_tema is not None and btn_tema.winfo_exists():
                btn_tema.configure(text=tema["texto_toggle"])

            if callback:
                try:
                    callback(tema)
                except Exception:
                    pass

    _VENTANAS_REGISTRADAS[:] = ventanas_vivas


def crear_boton_tema(ventana, padx=18, pady=(8, 2)):
    """
    Crea y ubica arriba a la derecha (anchor='ne') el botón interactivo 🌙 / ☀️.
    """
    tema = obtener_tema_actual()
    btn = ttk.Button(
        ventana,
        text=tema["texto_toggle"],
        style="Theme.TButton",
        command=alternar_tema
    )
    btn.pack(anchor="ne", padx=padx, pady=pady)
    ventana._btn_tema = btn
    return btn


def configurar_estilos_modernos(ventana, callback_tema=None):
    """
    Función que inicializa la estética visual en cualquier ventana que se abra:
    1. Coloca detrás de todo la imagen 'fondo.jpg' difuminada.
    2. Aplica los estilos de colores y tipografías Roboto.
    3. Conecta los eventos de clic de mouse para agrandar la letra de los botones al presionarlos.
    """
    tema = obtener_tema_actual()
    ventana.configure(bg=tema["fondo_app"])

    # 1. Creamos la etiqueta de fondo que ocupa el 100% del ancho y alto (relwidth=1, relheight=1)
    if getattr(ventana, "_lbl_fondo", None) is None:
        lbl_fondo = tk.Label(ventana, bg=tema["fondo_app"], bd=0, highlightthickness=0)
        lbl_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        lbl_fondo.lower()
        ventana._lbl_fondo = lbl_fondo
        ventana._ultimo_tam_fondo = (0, 0)

        # Si el usuario redimensiona la ventana, ajustamos suavemente la imagen de fondo
        def _al_redimensionar(event):
            if event.widget == ventana:
                ult_w, ult_h = getattr(ventana, "_ultimo_tam_fondo", (0, 0))
                if abs(event.width - ult_w) > 8 or abs(event.height - ult_h) > 8:
                    ventana._ultimo_tam_fondo = (event.width, event.height)
                    _actualizar_fondo_ventana(ventana, event.width, event.height)

        ventana.bind("<Configure>", _al_redimensionar, add="+")

    _actualizar_fondo_ventana(ventana)
    estilo = _aplicar_estilos_ttk(ventana)

    # 2. Aquí se maneja el efecto cuando el usuario presiona y suelta el clic sobre cualquier botón:
    def _al_presionar_boton(event):
        try:
            est_actual = str(event.widget.cget("style"))
            if est_actual != "Theme.TButton":
                # Al presionar el botón izquierdo del mouse, pasa a 'Pressed.TButton' (letra más grande)
                event.widget.configure(style="Pressed.TButton")
        except Exception:
            pass

    def _al_soltar_boton(event):
        try:
            est_actual = str(event.widget.cget("style"))
            if est_actual == "Pressed.TButton":
                # Al soltar el clic, vuelve al tamaño normal 'TButton'
                event.widget.configure(style="TButton")
        except Exception:
            pass

    ventana.bind_class("TButton", "<ButtonPress-1>", _al_presionar_boton, add="+")
    ventana.bind_class("TButton", "<ButtonRelease-1>", _al_soltar_boton, add="+")

    # 3. Registramos la ventana para que responda cuando se pulse el botón 🌙 / ☀️
    _VENTANAS_REGISTRADAS.append({
        "ventana": ventana,
        "callback": callback_tema
    })

    return estilo


# ----------------------------------------------------
# Persistencia de Datos en JSON (Lectura y Escritura)
# ----------------------------------------------------
def cargar_socios():
    """
    Lee el archivo 'clientes.json' y reconstruye la lista de objetos 'Socio'.
    Si el archivo no existe todavía, devuelve una lista vacía [] sin tirar error.
    """
    try:
        with open(RUTA_JSON, "r", encoding="utf-8") as f:
            datos = json.load(f)
            # '[Socio(**d) for d in datos]' convierte cada diccionario del JSON en un objeto Socio
            return [Socio(**d) for d in datos]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def guardar_socios(socios):
    """
    Convierte la lista de objetos 'Socio' a diccionarios y la guarda en 'clientes.json'.
    """
    with open(RUTA_JSON, "w", encoding="utf-8") as f:
        json.dump([s.to_dict() for s in socios], f, indent=4, ensure_ascii=False)


# ----------------------------------------------------
# Búsquedas (Simple y Múltiple para Homónimos)
# ----------------------------------------------------
def buscar_socio(criterio, socios=None):
    """
    Busca un socio por DNI exacto o coincidencia en Nombre/Apellido y devuelve el primero que encuentre.
    """
    lista = socios if socios is not None else cargar_socios()
    texto = str(criterio).strip().lower()

    for s in lista:
        if s.dni.lower() == texto:
            return s

    for s in lista:
        nombre_completo = f"{s.nombre} {s.apellido}".lower()
        if texto in s.nombre.lower() or texto in s.apellido.lower() or texto in nombre_completo:
            return s

    return None


def buscar_socios_coincidentes(criterio, socios=None):
    """
    Aquí se resuelve el problema de los homónimos (varios socios con el mismo nombre, ej: 'Jorge'):
    En lugar de detenerse en el primer resultado, recorre todo el padrón y devuelve una lista
    con TODAS las personas cuyo DNI, nombre o apellido coincidan con lo buscado.
    """
    lista = socios if socios is not None else cargar_socios()
    texto = str(criterio).strip().lower()
    if not texto:
        return []

    # Si escribió un DNI exacto, devolvemos ese socio puntual
    exactos_dni = [s for s in lista if s.dni.lower() == texto]
    if exactos_dni:
        return exactos_dni

    # Si escribió un nombre o apellido (ej: "Jorge"), juntamos todas las coincidencias encontradas
    coincidencias = []
    for s in lista:
        nombre_apellido = f"{s.nombre} {s.apellido}".lower()
        apellido_nombre = f"{s.apellido} {s.nombre}".lower()
        if (
            texto in s.dni.lower()
            or texto in s.nombre.lower()
            or texto in s.apellido.lower()
            or texto in nombre_apellido
            or texto in apellido_nombre
        ):
            coincidencias.append(s)

    return coincidencias


# ----------------------------------------------------
# Baja Individual/Múltiple, Edición y Filtros
# ----------------------------------------------------
def eliminar_socio(dni, socios=None):
    """Elimina a un único socio por su DNI."""
    return eliminar_socios_multiples([dni], socios) > 0


def eliminar_socios_multiples(lista_dnis, socios=None):
    """
    Elimina de 'clientes.json' a todos los socios cuyos DNIs estén dentro de 'lista_dnis'.
    Devuelve la cantidad total de socios eliminados.
    """
    lista = socios if socios is not None else cargar_socios()
    set_dnis = {str(d).strip() for d in lista_dnis}
    # Conservamos únicamente a los socios cuyo DNI NO esté en el conjunto de DNIs a borrar
    nueva_lista = [s for s in lista if s.dni not in set_dnis]
    eliminados = len(lista) - len(nueva_lista)

    if eliminados > 0:
        guardar_socios(nueva_lista)
    return eliminados


def actualizar_socio(dni_original, datos_actualizados):
    """
    Busca al socio por su 'dni_original', actualiza sus datos personales y deportivos
    y guarda los cambios en 'clientes.json'.
    """
    socios = cargar_socios()
    for s in socios:
        if s.dni == str(dni_original).strip():
            s.nombre = datos_actualizados.get("nombre", s.nombre)
            s.apellido = datos_actualizados.get("apellido", s.apellido)
            s.nacimiento = datos_actualizados.get("nacimiento", s.nacimiento)
            s.turno = datos_actualizados.get("turno", s.turno)
            s.apto_medico = datos_actualizados.get("apto_medico", s.apto_medico)
            s.estado = datos_actualizados.get("estado", s.estado)

            nueva_clase = datos_actualizados.get("clase", s.clase)
            if nueva_clase != s.clase:
                from datos import Actividad
                s.clase = nueva_clase
                s.actividad = Actividad(nueva_clase)

            guardar_socios(socios)
            return True
    return False


def filtrar_socios(texto_busqueda="", filtro_estado="Todos los socios", socios=None):
    """
    Filtra la lista de socios combinando lo que el usuario escribió en el buscador
    con la categoría elegida en el menú desplegable de la pantalla de estadísticas.
    """
    lista = socios if socios is not None else cargar_socios()
    resultado = []
    t = texto_busqueda.strip().lower()

    for s in lista:
        # 1. Comprobamos si coincide con el texto escrito en el buscador
        nombre_completo = f"{s.apellido} {s.nombre}".lower()
        coincide_texto = (
            not t
            or t in s.dni.lower()
            or t in s.nombre.lower()
            or t in s.apellido.lower()
            or t in nombre_completo
        )
        if not coincide_texto:
            continue

        # 2. Comprobamos si cumple con el filtro del desplegable
        estado_cuota = s.obtener_estado_cuota()
        necesita_aviso = s.necesita_aviso_cobro()
        apto_pendiente = s.actividad.requiere_apto and not s.apto_medico

        if filtro_estado == "Para avisar (Sin pago este mes)" and not necesita_aviso:
            continue
        if filtro_estado == "Atrasados (Morosos post día 10)" and estado_cuota != "Atrasado":
            continue
        if filtro_estado == "Al día" and estado_cuota != "Al día":
            continue
        if filtro_estado == "Con Apto Médico pendiente" and not apto_pendiente:
            continue
        if filtro_estado == "Turno Mañana" and s.turno != "Mañana":
            continue
        if filtro_estado == "Turno Tarde" and s.turno != "Tarde":
            continue

        resultado.append(s)

    return resultado


# ----------------------------------------------------
# Cálculos de Recaudación Mensual y Estadísticas
# ----------------------------------------------------
def calcular_recaudacion_mes(periodo=None, socios=None):
    """
    Suma todo el dinero recaudado en cuotas para un período mensual (por ejemplo: '10/2026').
    """
    lista = socios if socios is not None else cargar_socios()
    hoy = date.today()
    periodo_buscado = periodo or f"{hoy.month:02d}/{hoy.year}"

    total_ingresos = 0.0
    cantidad_pagos = 0
    detalles = []

    for s in lista:
        for pago in s.historial_pagos:
            p = str(pago.get("periodo", "")).strip()
            if p == periodo_buscado:
                monto = float(pago.get("monto", s.actividad.costo_mensual))
                total_ingresos += monto
                cantidad_pagos += 1
                detalles.append({
                    "dni": s.dni,
                    "socio": f"{s.apellido}, {s.nombre}",
                    "actividad": s.clase,
                    "turno": s.turno,
                    "fecha_pago": pago.get("fecha_pago", "-"),
                    "monto": monto
                })

    return {
        "periodo": periodo_buscado,
        "total_recaudado": total_ingresos,
        "cantidad_pagos": cantidad_pagos,
        "detalles": detalles
    }


def calcular_estadisticas(socios=None):
    """
    Cuenta cuántos alumnos hay en total, cuántos por actividad, cuántos por turno
    y cuántos están al día, pendientes o atrasados.
    """
    lista = socios if socios is not None else cargar_socios()
    total = len(lista)

    kayak = sum(1 for s in lista if s.clase == "Kayak")
    natacion = sum(1 for s in lista if s.clase == "Natación")
    ambas = sum(1 for s in lista if s.clase == "Ambas")

    turno_manana = sum(1 for s in lista if s.turno == "Mañana")
    turno_tarde = sum(1 for s in lista if s.turno == "Tarde")

    al_dia = sum(1 for s in lista if s.obtener_estado_cuota() == "Al día")
    pendientes = sum(1 for s in lista if "Pendiente" in s.obtener_estado_cuota())
    atrasados = sum(1 for s in lista if s.obtener_estado_cuota() == "Atrasado")
    apto_pendiente = sum(1 for s in lista if s.actividad.requiere_apto and not s.apto_medico)

    recaudacion = calcular_recaudacion_mes(socios=lista)

    return {
        "total": total,
        "kayak": kayak,
        "natacion": natacion,
        "ambas": ambas,
        "turno_manana": turno_manana,
        "turno_tarde": turno_tarde,
        "al_dia": al_dia,
        "pendientes": pendientes,
        "atrasados": atrasados,
        "apto_pendiente": apto_pendiente,
        "recaudacion_mes": recaudacion["total_recaudado"],
        "pagos_mes_cont": recaudacion["cantidad_pagos"]
    }


# ----------------------------------------------------
# Generación de Reportes en PDF con fpdf2
# ----------------------------------------------------
def generar_reporte_pdf(socios, ruta_destino=RUTA_PDF_GENERAL):
    """
    Genera el Reporte General en PDF (hoja A4 apaisada 'L') con el padrón completo
    de socios y un resumen estadístico al pie.
    """
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Título y fecha de emisión del PDF
    pdf.set_font("Helvetica", style="B", size=15)
    pdf.cell(0, 9, "SISTEMA NÁUTICO - REPORTE GENERAL DE SOCIOS", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", size=9)
    fecha_emision = datetime.now().strftime("%d/%m/%Y %H:%M")
    pdf.cell(0, 5, f"Fecha de emisión: {fecha_emision} | Día límite de cuota regular: 10 de cada mes", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # Cabecera de la tabla con fondo celeste claro RGB (220, 230, 245)
    pdf.set_font("Helvetica", style="B", size=8)
    pdf.set_fill_color(220, 230, 245)

    anchos = [22, 54, 22, 28, 20, 24, 26, 26, 38]
    columnas = ["DNI", "Apellido y Nombre", "F. Nac.", "Actividad", "Turno", "Apto Méd.", "Período", "F. Pago", "Estado Cuota"]

    for i, col in enumerate(columnas):
        pdf.cell(anchos[i], 7, col, border=1, align="C", fill=True)
    pdf.ln()

    # Filas de datos de cada socio
    pdf.set_font("Helvetica", size=8)
    for s in socios:
        nombre_completo = f"{s.apellido}, {s.nombre}"

        if s.actividad.requiere_apto:
            apto = "Sí (Vigente)" if s.apto_medico else "Falta certif."
        else:
            apto = "No requiere"

        estado_cuota = s.obtener_estado_cuota()
        periodo = s.periodo_abonado if s.periodo_abonado else "Sin reg."
        fecha_pago = s.fecha_pago if s.fecha_pago else "-"

        pdf.cell(anchos[0], 6, str(s.dni), border=1, align="C")
        pdf.cell(anchos[1], 6, nombre_completo[:26], border=1)
        pdf.cell(anchos[2], 6, str(s.nacimiento), border=1, align="C")
        pdf.cell(anchos[3], 6, str(s.clase), border=1, align="C")
        pdf.cell(anchos[4], 6, str(s.turno), border=1, align="C")
        pdf.cell(anchos[5], 6, apto, border=1, align="C")
        pdf.cell(anchos[6], 6, str(periodo), border=1, align="C")
        pdf.cell(anchos[7], 6, str(fecha_pago), border=1, align="C")
        pdf.cell(anchos[8], 6, estado_cuota, border=1, align="C")
        pdf.ln()

    # Resumen al pie del documento PDF
    stats = calcular_estadisticas(socios)
    pdf.ln(5)
    pdf.set_font("Helvetica", style="B", size=8)
    resumen_linea1 = (
        f"Totales: {stats['total']} socios  |  Kayak: {stats['kayak']}  |  Natación: {stats['natacion']}  |  "
        f"Ambas: {stats['ambas']}  |  Turno Mañana: {stats['turno_manana']}  |  Turno Tarde: {stats['turno_tarde']}"
    )
    resumen_linea2 = (
        f"Cuotas: {stats['al_dia']} Al día  |  {stats['pendientes']} Pendientes (Avisar antes del 10)  |  "
        f"{stats['atrasados']} Atrasados  |  Recaudación del mes: ${stats['recaudacion_mes']:,.2f} ({stats['pagos_mes_cont']} pagos)"
    )
    pdf.cell(0, 5, resumen_linea1, border="T", align="L", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, resumen_linea2, align="L")

    pdf.output(ruta_destino)
    return ruta_destino


def generar_reporte_avisos_pdf(socios, ruta_destino=RUTA_PDF_AVISOS):
    """
    Genera el PDF vertical ('P') exclusivamente con los socios que todavía adeudan
    el mes actual, sumando al final el monto total pendiente por cobrar.
    """
    pendientes = [s for s in socios if s.necesita_aviso_cobro()]

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Helvetica", style="B", size=15)
    pdf.cell(0, 9, "LISTADO DE COBRANZA Y RECORDATORIOS DE PAGO", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", size=9)
    hoy = date.today()
    fecha_emision = datetime.now().strftime("%d/%m/%Y %H:%M")

    motivo = (
        "RECORDATORIO PREVENTIVO (Vence el día 10)"
        if hoy.day <= 10
        else "LISTADO DE SOCIOS EN MORA (Pasó el día 10)"
    )
    pdf.cell(0, 5, f"Tipo: {motivo}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, f"Fecha de emisión: {fecha_emision}", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.set_font("Helvetica", style="B", size=9)
    pdf.set_fill_color(254, 237, 237)
    anchos = [25, 58, 28, 24, 28, 27]
    columnas = ["DNI", "Socio", "Actividad", "Turno", "Arancel", "Situación"]

    for i, col in enumerate(columnas):
        pdf.cell(anchos[i], 7, col, border=1, align="C", fill=True)
    pdf.ln()

    pdf.set_font("Helvetica", size=8)
    if not pendientes:
        pdf.cell(0, 10, "¡Excelente! No hay socios con cuota pendiente este mes.", border=1, align="C")
    else:
        total_a_cobrar = 0.0
        for s in pendientes:
            nombre = f"{s.apellido}, {s.nombre}"
            arancel = s.obtener_arancel_actual()
            total_a_cobrar += arancel
            situacion = s.obtener_estado_cuota()

            pdf.cell(anchos[0], 6, str(s.dni), border=1, align="C")
            pdf.cell(anchos[1], 6, nombre[:26], border=1)
            pdf.cell(anchos[2], 6, str(s.clase), border=1, align="C")
            pdf.cell(anchos[3], 6, str(s.turno), border=1, align="C")
            pdf.cell(anchos[4], 6, f"${arancel:,.2f}", border=1, align="C")
            pdf.cell(anchos[5], 6, situacion, border=1, align="C")
            pdf.ln()

        pdf.ln(3)
        pdf.set_font("Helvetica", style="B", size=9)
        pdf.cell(0, 6, f"Total pendiente a cobrar: ${total_a_cobrar:,.2f} ({len(pendientes)} socios)", border="T", align="R")

    pdf.output(ruta_destino)
    return ruta_destino
