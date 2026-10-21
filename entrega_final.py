"""
================================================================================
TRABAJO INTEGRADOR FINAL (TIF) - SISTEMA DE GESTIÓN NÁUTICA (KAYAK Y NATACIÓN)
ARCHIVO UNIFICADO Y COMENTADO LÍNEA POR LÍNEA PARA DEFENSA ORAL: entrega_final.py
================================================================================

ESTRUCTURA DE ESTE ARCHIVO AUTOCONTENIDO:
Este script integra los 7 módulos del proyecto en el orden exacto de dependencias
para que funcione por sí solo y puedas abrirlo durante tu defensa oral para
explicar cualquier línea ante el profesor:

  • SECCIÓN 1 (Equivalente a 'datos.py'):
    Modelo de Objetos (POO) con las clases 'Actividad' y 'Socio', reglas de
    negocio (vencimiento el día 10, apto médico obligatorio en Natación/Ambas)
    y lectura/escritura de 'precios.json'.

  • SECCIÓN 2 (Equivalente a 'logica.py'):
    Motor Visual e Interactivo (paleta de tonos azules #779be7 y #49b6ff con
    acentos leves en rosa pétalo #d264b6, fuente limpia 'Roboto', imagen de
    fondo 'fondo.jpg' difuminada con Pillow, conmutador Modo Día ☀️ / Modo Noche 🌙,
    efectos Hover y crecimiento tipográfico en botones), persistencia en
    'clientes.json', búsqueda múltiple de homónimos y reportes PDF con 'fpdf2'.

  • SECCIÓN 3 (Equivalente a 'pantalla_clientes.py'):
    Ventana emergente de Alta de Nuevos Alumnos / Socios con validaciones.

  • SECCIÓN 4 (Equivalente a 'pantalla_precios.py'):
    Ventana emergente para configurar los importes mensuales de las cuotas.

  • SECCIÓN 5 (Equivalente a 'pantalla_edicion.py'):
    Ventana emergente modal para modificar los datos de un alumno existente.

  • SECCIÓN 6 (Equivalente a 'pantalla_renovacion.py'):
    Ventana de Registro de Cobro de Cuota con resolución dinámica de homónimos.

  • SECCIÓN 7 (Equivalente a 'pantalla_estadisticas.py'):
    Panel de Consultas, Métricas, Recaudación, Filtros en tiempo real, Tabla
    interactiva 'Treeview', Baja múltiple y exportación de Reportes PDF.

  • SECCIÓN 8 (Equivalente a 'main.py'):
    Ventana Principal (Dashboard), Barra de Menús Desplegables, Conmutador de
    Tema (☀️ / 🌙), Tarjeta de Estado en Vivo y Accesos Rápidos.
================================================================================
"""

# ==============================================================================
# IMPORTACIONES GENERALES DEL SISTEMA
# ==============================================================================
# Aquí importamos 'os' para ubicar carpetas/archivos y abrir los PDFs generados en Windows
import os
# Aquí importamos 'json' para leer y guardar nuestras bases de datos ('clientes.json' y 'precios.json')
import json
# Aquí importamos 'date' y 'datetime' para manejar la fecha real de hoy y validar formatos DD/MM/AAAA
from datetime import date, datetime
# Aquí importamos 'tkinter' (como 'tk') para crear las ventanas, menús y listas
import tkinter as tk
# Aquí importamos 'ttk' (controles modernos estilizados) y 'messagebox' (cuadros de diálogo y alertas)
from tkinter import ttk, messagebox
# Aquí importamos 'FPDF' (de la librería 'fpdf2') para diseñar y exportar los reportes en formato PDF
from fpdf import FPDF

# Aquí importamos Pillow ('PIL') para abrir la imagen 'fondo.jpg', aplicarle desenfoque Gaussiano
# y convertirla con 'ImageTk' para mostrarla como fondo suave en Tkinter.
# El bloque 'try...except' garantiza que si en una PC no está instalado Pillow, el programa funcione igual.
try:
    from PIL import Image, ImageTk, ImageFilter
    PILLOW_DISPONIBLE = True
except ImportError:
    PILLOW_DISPONIBLE = False

# ==============================================================================
# CONFIGURACIÓN DE RUTAS DE ARCHIVOS
# ==============================================================================
# Aquí obtenemos la ruta exacta de la carpeta donde está guardado este archivo .py
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
# Aquí definimos las rutas completas hacia los archivos JSON, los PDFs y la imagen de fondo
RUTA_PRECIOS = os.path.join(DIRECTORIO_ACTUAL, "precios.json")
RUTA_JSON = os.path.join(DIRECTORIO_ACTUAL, "clientes.json")
RUTA_PDF_GENERAL = os.path.join(DIRECTORIO_ACTUAL, "reporte_socios.pdf")
RUTA_PDF_AVISOS = os.path.join(DIRECTORIO_ACTUAL, "reporte_avisos_cobro.pdf")
RUTA_IMAGEN_FONDO = os.path.join(DIRECTORIO_ACTUAL, "fondo.jpg")


# ==============================================================================
# SECCIÓN 1: MODELO DE DATOS Y PROGRAMACIÓN ORIENTADA A OBJETOS (datos.py)
# ==============================================================================
"""
1. PROPÓSITO GENERAL DE ESTA SECCIÓN:
   Es el "cerebro conceptual" del sistema. Define las clases 'Actividad' y 'Socio'
   aplicando Programación Orientada a Objetos (POO) y gestiona el archivo 'precios.json'.

2. ELEMENTOS VISUALES / INTERFAZ:
   No dibuja ventanas, pero produce los textos de estado que se ven en la tabla y
   en las tarjetas: "Al día", "Pendiente (Vence el 10)" y "Atrasado".
"""

# Aquí se definen los precios iniciales por defecto (diccionario clave: valor)
# Sirven como respaldo automático si todavía no existe o se borra el archivo 'precios.json'
PRECIOS_PREDETERMINADOS = {
    "Kayak": 15000.0,
    "Natación": 18000.0,
    "Ambas": 28000.0
}


def cargar_precios():
    """
    Función que lee los precios de las cuotas desde el archivo 'precios.json'.
    Si el archivo no existe, lo crea automáticamente con los valores predeterminados.
    """
    # El bloque 'try' intenta abrir y leer el archivo 'precios.json'
    try:
        # Abrimos 'precios.json' en modo lectura ("r") y con codificación "utf-8" para admitir tildes
        with open(RUTA_PRECIOS, "r", encoding="utf-8") as f:
            # Convertimos el texto del archivo JSON en un diccionario de Python
            precios = json.load(f)
            # Recorremos los precios predeterminados para asegurarnos de que no falte ninguna actividad
            for k, v in PRECIOS_PREDETERMINADOS.items():
                if k not in precios:
                    precios[k] = v
            # Devolvemos el diccionario con los precios listos para usar
            return precios
    # Si el archivo no existe (FileNotFoundError) o está vacío/dañado (JSONDecodeError), entra aquí:
    except (FileNotFoundError, json.JSONDecodeError):
        # Crea automáticamente el archivo 'precios.json' con los precios por defecto
        guardar_precios(PRECIOS_PREDETERMINADOS)
        # Devuelve una copia de los precios predeterminados para que el programa siga funcionando
        return PRECIOS_PREDETERMINADOS.copy()


def guardar_precios(nuevos_precios):
    """
    Función que guarda los aranceles actualizados dentro del archivo 'precios.json'.
    Se ejecuta cuando el usuario modifica los importes desde la ventana de precios.
    """
    # Abrimos 'precios.json' en modo escritura ("w"), lo que actualiza su contenido
    with open(RUTA_PRECIOS, "w", encoding="utf-8") as f:
        # Guardamos el diccionario en formato JSON con sangría de 4 espacios (indent=4)
        # y permitiendo tildes y eñes (ensure_ascii=False)
        json.dump(nuevos_precios, f, indent=4, ensure_ascii=False)


class Actividad:
    """
    Clase que representa una disciplina deportiva disponible en el club.
    Puede ser 'Kayak', 'Natación' o 'Ambas' (Kayak + Natación).
    """
    # '__init__' es el constructor: se ejecuta automáticamente cuando creamos una nueva Actividad
    def __init__(self, nombre, costo_mensual=None, requiere_apto=None):
        # Guardamos el nombre de la actividad ("Kayak", "Natación" o "Ambas") en el objeto (self)
        self.nombre = nombre
        # Leemos los precios actuales desde 'precios.json'
        precios = cargar_precios()

        # Aquí se asigna el precio mensual de la actividad:
        # Si no nos pasaron un costo manual, buscamos el precio correspondiente en 'precios.json'
        if costo_mensual is None:
            self.costo_mensual = float(precios.get(nombre, 15000.0))
        else:
            # Si nos pasaron un costo específico, lo convertimos a número con decimales (float)
            self.costo_mensual = float(costo_mensual)

        # Aquí se define la regla de negocio del Apto Médico:
        # Si practica 'Natación' o 'Ambas', el certificado médico es obligatorio (True).
        # Si solo practica 'Kayak', no es obligatorio (False).
        if requiere_apto is None:
            self.requiere_apto = nombre in ("Natación", "Ambas")
        else:
            self.requiere_apto = bool(requiere_apto)

    def to_dict(self):
        """Convierte los datos de la actividad a un diccionario común de Python."""
        return {
            "nombre": self.nombre,
            "costo_mensual": self.costo_mensual,
            "requiere_apto": self.requiere_apto
        }

    def __str__(self):
        """Define cómo se muestra la actividad si la convertimos a texto (ej: 'Kayak ($15,000.00)')."""
        return f"{self.nombre} (${self.costo_mensual:,.2f})"


class Socio:
    """
    Clase principal que representa a un alumno o socio del club náutico.
    Agrupa sus datos personales, su turno, su actividad deportiva y sus pagos de cuotas.
    """
    # Constructor que recibe todos los datos de un socio al crearlo o al cargarlo desde 'clientes.json'
    def __init__(self, dni, nombre, apellido, fecha_de_nacimiento, clase="Kayak",
                 apto_medico=False, estado="Activo", cuota_al_dia=False,
                 mes_abonado="", dia_pago=0, periodo_abonado="", fecha_pago="",
                 turno="Mañana", historial_pagos=None, monto_ultimo_pago=0.0):
        # Aquí guardamos los datos personales convirtiéndolos a texto (str) y quitando espacios extra (.strip())
        self.dni = str(dni).strip()
        self.nombre = str(nombre).strip()
        self.apellido = str(apellido).strip()
        self.nacimiento = str(fecha_de_nacimiento).strip()

        # Aquí guardamos el turno al que asiste el alumno ('Mañana' o 'Tarde')
        self.turno = str(turno).strip() if turno else "Mañana"

        # Aquí aplicamos COMPOSICIÓN en POO: cada Socio tiene adentro un objeto de la clase 'Actividad'
        if isinstance(clase, Actividad):
            self.actividad = clase
            self.clase = clase.nombre
        else:
            self.clase = str(clase)
            # Creamos el objeto Actividad según el nombre del deporte elegido ("Kayak", "Natación" o "Ambas")
            self.actividad = Actividad(self.clase)

        # Aquí guardamos si entregó el apto médico (True = Sí, False = No) y si está 'Activo' o 'Inactivo'
        self.apto_medico = bool(apto_medico)
        self.estado = estado

        # Aquí guardamos la información del último período de cuota que pagó (ej: "10/2026")
        self.periodo_abonado = periodo_abonado or mes_abonado
        # Aquí guardamos la fecha en que realizó ese último pago (ej: "20/10/2026")
        self.fecha_pago = fecha_pago
        # Aquí guardamos cuánto dinero abonó en su último pago
        self.monto_ultimo_pago = float(monto_ultimo_pago) if monto_ultimo_pago else 0.0

        # Aquí se configura la lista del historial de todos los pagos realizados por este socio
        if historial_pagos is not None and isinstance(historial_pagos, list):
            self.historial_pagos = historial_pagos
        else:
            self.historial_pagos = []
            # Si el socio venía de un registro anterior y ya tenía un período abonado, lo sumamos al historial
            if self.periodo_abonado:
                self.historial_pagos.append({
                    "periodo": self.periodo_abonado,
                    "fecha_pago": self.fecha_pago or "Histórico",
                    "monto": self.actividad.costo_mensual
                })

        # Atributos adicionales de compatibilidad para conservar el formato completo en el JSON
        self.mes_abonado = mes_abonado or self.periodo_abonado
        self.dia_pago = dia_pago
        self.cuota_al_dia = cuota_al_dia

    def obtener_arancel_actual(self):
        """
        Consulta el archivo 'precios.json' y devuelve cuánto debe pagar hoy este socio
        según la actividad que realiza (Kayak, Natación o Ambas).
        """
        precios = cargar_precios()
        return float(precios.get(self.clase, self.actividad.costo_mensual))

    def obtener_periodo_actual(self, fecha_referencia=None):
        """
        Obtiene el mes y año actual en formato 'MM/AAAA' (por ejemplo: '10/2026').
        El ':02d' asegura que los meses del 1 al 9 tengan un cero adelante (ej: '04/2026').
        """
        ref = fecha_referencia or date.today()
        return f"{ref.month:02d}/{ref.year}"

    def tiene_mes_abonado(self, fecha_referencia=None):
        """
        Verifica si el socio ya pagó la cuota correspondiente al mes actual.
        Devuelve True si pagó, o False si todavía debe el mes.
        """
        # Tomamos la fecha de hoy y calculamos el período actual (ej: '10/2026')
        ref = fecha_referencia or date.today()
        periodo_actual = self.obtener_periodo_actual(ref)

        # Lista de nombres de meses por si algún registro histórico se guardó con el nombre del mes
        meses_nombres = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        nombre_mes_actual = meses_nombres[ref.month - 1]

        # 1. Revisamos si el último período abonado coincide con el mes actual
        p_actual = str(self.periodo_abonado).strip()
        if p_actual == periodo_actual or p_actual.lower() == nombre_mes_actual.lower():
            return True

        # 2. Revisamos también dentro de toda su lista de pagos (historial_pagos)
        for pago in self.historial_pagos:
            p = str(pago.get("periodo", "")).strip()
            if p == periodo_actual or p.lower() == nombre_mes_actual.lower():
                return True

        # Si no se encontró el pago de este mes, devuelve False
        return False

    def obtener_estado_cuota(self, fecha_referencia=None):
        """
        Calcula automáticamente la situación de pago del socio según el día del mes:
        - Si ya pagó este mes -> Devuelve 'Al día'.
        - Si no pagó, pero hoy es del día 1 al 10 -> Devuelve 'Pendiente (Vence el 10)'.
        - Si no pagó y ya pasamos el día 10 -> Devuelve 'Atrasado'.
        """
        ref = fecha_referencia or date.today()

        # Si ya abonó el mes actual, está al día sin importar qué fecha sea hoy
        if self.tiene_mes_abonado(ref):
            return "Al día"

        # Si todavía no pagó este mes, miramos qué día del mes es hoy (ref.day)
        if ref.day <= 10:
            # Del 1 al 10 todavía está dentro del plazo regular de pago
            return "Pendiente (Vence el 10)"
        else:
            # Del 11 en adelante ya venció el plazo y pasa a estar en mora
            return "Atrasado"

    def esta_al_dia(self, fecha_referencia=None):
        """Devuelve True únicamente si el estado de la cuota es 'Al día'."""
        return self.obtener_estado_cuota(fecha_referencia) == "Al día"

    def necesita_aviso_cobro(self, fecha_referencia=None):
        """
        Devuelve True si el socio todavía no pagó el mes actual (ya sea 'Pendiente' o 'Atrasado').
        Se utiliza para generar el listado PDF de avisos y cobranzas.
        """
        return not self.tiene_mes_abonado(fecha_referencia)

    def tiene_apto_valido(self):
        """
        Comprueba si el alumno cumple con el requisito del certificado médico:
        - Si su actividad lo exige (Natación o Ambas), devuelve True solo si lo entregó.
        - Si hace solo Kayak, devuelve siempre True porque no requiere certificado.
        """
        if self.actividad.requiere_apto:
            return self.apto_medico
        return True

    def esta_habilitado_para_ingreso(self, fecha_referencia=None):
        """
        Evalúa si el alumno tiene permitido entrar hoy a la clase en el agua:
        Verifica que esté 'Activo', que tenga el apto médico al día y que no tenga la cuota vencida.
        """
        if self.estado != "Activo":
            return False, "Socio inactivo"
        if not self.tiene_apto_valido():
            return False, "Falta certificado médico (obligatorio para Natación y Ambas)"
        if self.obtener_estado_cuota(fecha_referencia) == "Atrasado":
            return False, "Cuota atrasada (venció el día 10)"
        return True, "Habilitado para ingresar"

    def registrar_pago(self, periodo, fecha_pago=None, monto=None):
        """
        Aquí se maneja el registro de un nuevo cobro de cuota en la ficha del socio:
        Actualiza su período abonado, la fecha de pago, el importe y agrega el recibo al historial.
        """
        # Guardamos el período que está pagando (ej: '10/2026')
        self.periodo_abonado = periodo
        self.mes_abonado = periodo
        # Guardamos la fecha en que pagó (o la fecha de hoy si no se especificó otra)
        self.fecha_pago = fecha_pago or date.today().strftime("%d/%m/%Y")

        # Convertimos el monto pagado a número decimal (float)
        arancel = float(monto) if monto is not None else self.obtener_arancel_actual()
        self.monto_ultimo_pago = arancel

        # Extraemos el número del día (ej: 20) a partir de la fecha "20/10/2026"
        try:
            self.dia_pago = int(self.fecha_pago.split("/")[0])
        except (ValueError, IndexError):
            self.dia_pago = date.today().day

        # Creamos el comprobante como diccionario y lo agregamos a su lista 'historial_pagos'
        registro = {
            "periodo": periodo,
            "fecha_pago": self.fecha_pago,
            "monto": arancel
        }
        self.historial_pagos.append(registro)
        # Actualizamos la bandera que indica que su cuota está al día
        self.cuota_al_dia = self.esta_al_dia()

    def to_dict(self):
        """
        Empaqueta todos los datos del objeto Socio dentro de un diccionario de Python.
        Esto es indispensable porque el formato JSON solo entiende diccionarios y listas.
        """
        return {
            "dni": self.dni,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha_de_nacimiento": self.nacimiento,
            "clase": self.clase,
            "turno": self.turno,
            "apto_medico": self.apto_medico,
            "estado": self.estado,
            "cuota_al_dia": self.esta_al_dia(),
            "mes_abonado": self.mes_abonado,
            "dia_pago": self.dia_pago,
            "periodo_abonado": self.periodo_abonado,
            "fecha_pago": self.fecha_pago,
            "monto_ultimo_pago": self.monto_ultimo_pago,
            "historial_pagos": self.historial_pagos
        }


# ==============================================================================
# SECCIÓN 2: MOTOR VISUAL, BÚSQUEDAS, ESTADÍSTICAS Y REPORTES PDF (logica.py)
# ==============================================================================
"""
1. PROPÓSITO GENERAL DE ESTA SECCIÓN:
   - Configura toda la estética visual del sistema: paleta con predominio de azules
     (#779be7 y #49b6ff) y acentos rosas sutiles (#d264b6), fuente limpia 'Roboto',
     imagen 'fondo.jpg' difuminada con Pillow, alternancia Modo Día / Modo Noche y
     efectos dinámicos en botones (Hover y crecimiento de letra al hacer clic).
   - Gestiona 'clientes.json', la búsqueda de homónimos, los filtros, la recaudación
     mensual y la exportación de los 2 reportes en PDF.
"""

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


# ==============================================================================
# SECCIÓN 3: ALTA DE NUEVOS ALUMNOS / SOCIOS (pantalla_clientes.py)
# ==============================================================================
"""
1. PROPÓSITO GENERAL DE ESTA SECCIÓN:
   Abre la ventana emergente para inscribir a un nuevo alumno, validando todos
   los campos antes de guardarlo en 'clientes.json'.
"""


def abrir_pantalla_clientes(root, callback_actualizar=None):
    """
    Función que construye y abre la ventana emergente para registrar un nuevo alumno.
    Recibe 'root' (la ventana principal) y 'callback_actualizar' (para refrescar el inicio al guardar).
    """
    # Aquí se crea una ventana secundaria ('Toplevel') dependiente de la ventana principal
    ventana = tk.Toplevel(root)
    ventana.title("Alta de Socio - Sistema Náutico")
    # Aquí se define el tamaño de la ventana: 480 píxeles de ancho por 500 píxeles de alto
    ventana.geometry("480x500")
    # Aquí bloqueamos el cambio de tamaño manual para que no se desarme la grilla
    ventana.resizable(False, False)
    # 'grab_set()' hace que la ventana sea "modal"
    ventana.grab_set()

    # Aquí aplicamos la imagen de fondo difuminada, los colores azules y los efectos en los botones
    configurar_estilos_modernos(ventana)
    # Aquí agregamos el botón 🌙 / ☀️ arriba a la derecha para cambiar entre Modo Día y Modo Noche
    crear_boton_tema(ventana, padx=18, pady=(10, 2))

    # Aquí se crea la tarjeta principal ('LabelFrame') que contiene todo el formulario
    frame = ttk.LabelFrame(ventana, text=" ✨ Datos del Nuevo Alumno / Socio ", padding=15)
    frame.pack(fill="both", expand=True, padx=18, pady=(4, 16))

    # --- FILA 0: Campo DNI ---
    ttk.Label(frame, text="DNI (solo números):", style="Card.TLabel").grid(row=0, column=0, padx=8, pady=6, sticky="e")
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
    combo_clase = ttk.Combobox(frame, values=["Kayak", "Natación", "Ambas"], state="readonly", width=19)
    combo_clase.grid(row=4, column=1, padx=8, pady=6, sticky="w")
    combo_clase.set("Kayak")

    # --- FILA 5: Lista Desplegable de Turno ---
    ttk.Label(frame, text="Turno:", style="Card.TLabel").grid(row=5, column=0, padx=8, pady=6, sticky="e")
    combo_turno = ttk.Combobox(frame, values=["Mañana", "Tarde"], state="readonly", width=19)
    combo_turno.grid(row=5, column=1, padx=8, pady=6, sticky="w")
    combo_turno.set("Mañana")

    # --- FILA 6: Lista Desplegable de Apto Médico ---
    lbl_apto = ttk.Label(frame, text="Apto Médico:", style="Card.TLabel")
    lbl_apto.grid(row=6, column=0, padx=8, pady=6, sticky="e")
    combo_apto = ttk.Combobox(frame, values=["No requiere"], state="readonly", width=19)
    combo_apto.grid(row=6, column=1, padx=8, pady=6, sticky="w")
    combo_apto.set("No requiere")

    # Aquí se maneja lo que pasa cuando el usuario cambia la Actividad en el desplegable:
    def al_cambiar_actividad(event=None):
        actividad = combo_clase.get()
        if actividad in ("Natación", "Ambas"):
            combo_apto.config(values=["Sí (Entregado)", "No (Pendiente)"])
            combo_apto.set("No (Pendiente)")
        else:
            combo_apto.config(values=["No requiere"])
            combo_apto.set("No requiere")

    combo_clase.bind("<<ComboboxSelected>>", al_cambiar_actividad)

    # Aquí se maneja lo que pasa cuando el usuario hace clic en el botón "💾 Guardar Socio":
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

        # Validación 2: DNI numérico de 7 a 9 dígitos
        if not dni.isdigit() or len(dni) < 7 or len(dni) > 9:
            messagebox.showerror("Error", "El DNI debe contener únicamente entre 7 y 9 dígitos.", parent=ventana)
            return

        # Validación 3: Fecha real en formato DD/MM/AAAA
        try:
            datetime.strptime(fecha, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "La fecha de nacimiento debe tener el formato DD/MM/AAAA (ej: 20/04/2002).", parent=ventana)
            return

        socios = cargar_socios()

        # Validación 4: DNI único no repetido
        if any(s.dni == dni for s in socios):
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

    # --- FILA 7: Botones de Guardar y Cancelar ---
    frame_botones = ttk.Frame(frame, style="Card.TFrame")
    frame_botones.grid(row=7, column=0, columnspan=2, pady=(16, 4))

    btn_guardar = ttk.Button(frame_botones, text="💾 Guardar Socio", command=guardar)
    btn_guardar.pack(side="left", padx=6)

    btn_cancelar = ttk.Button(frame_botones, text="Cancelar", command=ventana.destroy)
    btn_cancelar.pack(side="left", padx=6)


# ==============================================================================
# SECCIÓN 4: CONFIGURACIÓN DE IMPORTES DE CUOTAS (pantalla_precios.py)
# ==============================================================================
"""
1. PROPÓSITO GENERAL DE ESTA SECCIÓN:
   Permite consultar y modificar el valor mensual en pesos ($) de las cuotas de
   Kayak, Natación y Ambas, guardando los cambios en 'precios.json'.
"""


def abrir_pantalla_precios(root, callback_actualizar=None):
    """
    Abre la ventana emergente para editar los importes mensuales de las cuotas.
    """
    ventana = tk.Toplevel(root)
    ventana.title("Configuración de Aranceles de Cuotas")
    ventana.geometry("430x360")
    ventana.resizable(False, False)
    ventana.grab_set()

    configurar_estilos_modernos(ventana)
    crear_boton_tema(ventana, padx=18, pady=(10, 2))

    frame = ttk.LabelFrame(ventana, text=" 💲 Modificación de Importes Mensuales ($) ", padding=15)
    frame.pack(fill="both", expand=True, padx=18, pady=(4, 16))

    precios_actuales = cargar_precios()

    # --- FILA 0: Precio de Kayak ---
    ttk.Label(frame, text="Cuota Kayak ($):", style="Card.TLabel").grid(row=0, column=0, padx=10, pady=8, sticky="e")
    entry_kayak = ttk.Entry(frame, width=16)
    entry_kayak.grid(row=0, column=1, padx=10, pady=8, sticky="w")
    entry_kayak.insert(0, str(precios_actuales.get("Kayak", 15000.0)))

    # --- FILA 1: Precio de Natación ---
    ttk.Label(frame, text="Cuota Natación ($):", style="Card.TLabel").grid(row=1, column=0, padx=10, pady=8, sticky="e")
    entry_natacion = ttk.Entry(frame, width=16)
    entry_natacion.grid(row=1, column=1, padx=10, pady=8, sticky="w")
    entry_natacion.insert(0, str(precios_actuales.get("Natación", 18000.0)))

    # --- FILA 2: Precio de Ambas Actividades ---
    ttk.Label(frame, text="Cuota Ambas (Combo) ($):", style="Card.TLabel").grid(row=2, column=0, padx=10, pady=8, sticky="e")
    entry_ambas = ttk.Entry(frame, width=16)
    entry_ambas.grid(row=2, column=1, padx=10, pady=8, sticky="w")
    entry_ambas.insert(0, str(precios_actuales.get("Ambas", 28000.0)))

    # Aquí se maneja lo que pasa cuando el usuario hace clic en "💾 Guardar Cambios":
    def guardar():
        try:
            val_kayak = float(entry_kayak.get().strip().replace(",", "."))
            val_natacion = float(entry_natacion.get().strip().replace(",", "."))
            val_ambas = float(entry_ambas.get().strip().replace(",", "."))

            if val_kayak <= 0 or val_natacion <= 0 or val_ambas <= 0:
                messagebox.showerror("Error", "Los importes deben ser mayores a cero.", parent=ventana)
                return

            nuevos = {
                "Kayak": val_kayak,
                "Natación": val_natacion,
                "Ambas": val_ambas
            }
            guardar_precios(nuevos)

            messagebox.showinfo(
                "Aranceles Actualizados",
                "Los nuevos importes fueron guardados exitosamente en 'precios.json'.\n"
                "Se aplicarán a los nuevos cobros.",
                parent=ventana
            )

            if callback_actualizar:
                callback_actualizar()
            ventana.destroy()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos.", parent=ventana)

    # --- FILA 3: Botones de Guardar y Cancelar ---
    frame_botones = ttk.Frame(frame, style="Card.TFrame")
    frame_botones.grid(row=3, column=0, columnspan=2, pady=(16, 4))

    btn_guardar = ttk.Button(frame_botones, text="💾 Guardar Cambios", command=guardar)
    btn_guardar.pack(side="left", padx=6)

    btn_cancelar = ttk.Button(frame_botones, text="Cancelar", command=ventana.destroy)
    btn_cancelar.pack(side="left", padx=6)


# ==============================================================================
# SECCIÓN 5: MODIFICACIÓN DE DATOS DE UN ALUMNO (pantalla_edicion.py)
# ==============================================================================
"""
1. PROPÓSITO GENERAL DE ESTA SECCIÓN:
   Permite editar los datos personales, actividad, turno, apto médico o estado
   (Activo/Inactivo) de un alumno seleccionado en la tabla de estadísticas.
"""


def abrir_pantalla_edicion(root, socio, callback_actualizar=None):
    """
    Abre una ventana emergente modal con los datos precargados del 'socio' elegido.
    """
    if not socio:
        messagebox.showwarning("Atención", "No se especificó ningún alumno para modificar.")
        return

    ventana = tk.Toplevel(root)
    ventana.title(f"Modificar Alumno - DNI: {socio.dni}")
    ventana.geometry("480x530")
    ventana.resizable(False, False)
    ventana.grab_set()

    configurar_estilos_modernos(ventana)
    crear_boton_tema(ventana, padx=18, pady=(10, 2))

    frame = ttk.LabelFrame(
        ventana,
        text=f" ✏️ Editando Socio: {socio.nombre} {socio.apellido} ",
        padding=15
    )
    frame.pack(fill="both", expand=True, padx=18, pady=(4, 16))

    # --- FILA 0: DNI (Deshabilitado para proteger el identificador único) ---
    ttk.Label(frame, text="DNI:", style="Card.TLabel").grid(row=0, column=0, padx=8, pady=6, sticky="e")
    entry_dni = ttk.Entry(frame, width=22)
    entry_dni.grid(row=0, column=1, padx=8, pady=6, sticky="w")
    entry_dni.insert(0, str(socio.dni))
    entry_dni.config(state="disabled")

    # --- FILA 1: Nombre ---
    ttk.Label(frame, text="Nombre:", style="Card.TLabel").grid(row=1, column=0, padx=8, pady=6, sticky="e")
    entry_nombre = ttk.Entry(frame, width=22)
    entry_nombre.grid(row=1, column=1, padx=8, pady=6, sticky="w")
    entry_nombre.insert(0, socio.nombre)

    # --- FILA 2: Apellido ---
    ttk.Label(frame, text="Apellido:", style="Card.TLabel").grid(row=2, column=0, padx=8, pady=6, sticky="e")
    entry_apellido = ttk.Entry(frame, width=22)
    entry_apellido.grid(row=2, column=1, padx=8, pady=6, sticky="w")
    entry_apellido.insert(0, socio.apellido)

    # --- FILA 3: Fecha de Nacimiento ---
    ttk.Label(frame, text="F. Nac. (DD/MM/AAAA):", style="Card.TLabel").grid(row=3, column=0, padx=8, pady=6, sticky="e")
    entry_fecha = ttk.Entry(frame, width=22)
    entry_fecha.grid(row=3, column=1, padx=8, pady=6, sticky="w")
    entry_fecha.insert(0, str(socio.nacimiento))

    # --- FILA 4: Actividad ---
    ttk.Label(frame, text="Actividad:", style="Card.TLabel").grid(row=4, column=0, padx=8, pady=6, sticky="e")
    combo_clase = ttk.Combobox(frame, values=["Kayak", "Natación", "Ambas"], state="readonly", width=19)
    combo_clase.grid(row=4, column=1, padx=8, pady=6, sticky="w")
    combo_clase.set(socio.clase if socio.clase in ("Kayak", "Natación", "Ambas") else "Kayak")

    # --- FILA 5: Turno ---
    ttk.Label(frame, text="Turno:", style="Card.TLabel").grid(row=5, column=0, padx=8, pady=6, sticky="e")
    combo_turno = ttk.Combobox(frame, values=["Mañana", "Tarde"], state="readonly", width=19)
    combo_turno.grid(row=5, column=1, padx=8, pady=6, sticky="w")
    combo_turno.set(socio.turno if socio.turno in ("Mañana", "Tarde") else "Mañana")

    # --- FILA 6: Apto Médico ---
    ttk.Label(frame, text="Apto Médico:", style="Card.TLabel").grid(row=6, column=0, padx=8, pady=6, sticky="e")
    combo_apto = ttk.Combobox(frame, values=["Sí (Entregado)", "No (Pendiente)", "No requiere"], state="readonly", width=19)
    combo_apto.grid(row=6, column=1, padx=8, pady=6, sticky="w")

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

    # --- FILA 7: Estado ---
    ttk.Label(frame, text="Estado:", style="Card.TLabel").grid(row=7, column=0, padx=8, pady=6, sticky="e")
    combo_estado = ttk.Combobox(frame, values=["Activo", "Inactivo"], state="readonly", width=19)
    combo_estado.grid(row=7, column=1, padx=8, pady=6, sticky="w")
    combo_estado.set(socio.estado if socio.estado in ("Activo", "Inactivo") else "Activo")

    # Aquí se maneja lo que pasa cuando el usuario hace clic en "💾 Guardar Cambios":
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
            messagebox.showinfo("Modificación Exitosa", f"Los datos de {nombre} {apellido} fueron actualizados correctamente.", parent=ventana)
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


# ==============================================================================
# SECCIÓN 6: COBRO DE CUOTAS Y RESOLUCIÓN DE HOMÓNIMOS (pantalla_renovacion.py)
# ==============================================================================
"""
1. PROPÓSITO GENERAL DE ESTA SECCIÓN:
   Permite buscar a un socio por DNI o Nombre para cobrarle la cuota. Si hay más
   de una persona con el mismo nombre (homónimos), despliega una lista interactiva
   para seleccionar al socio correcto, carga su arancel y registra el pago.
"""


def abrir_pantalla_renovacion(root, callback_actualizar=None):
    """
    Abre la ventana emergente para buscar a un socio (resolviendo homónimos) y cobrar su cuota.
    """
    ventana = tk.Toplevel(root)
    ventana.title("Registro de Cobro de Cuota - Sistema Náutico")
    ventana.geometry("560x640")
    ventana.minsize(530, 590)
    ventana.grab_set()

    # Diccionario interno para recordar el socio elegido y la lista de homónimos encontrados
    estado_busqueda = {
        "socio": None,
        "coincidencias": []
    }

    tema_inicial = obtener_tema_actual()
    crear_boton_tema(ventana, padx=18, pady=(8, 2))

    # ----------------------------------------------------
    # 1. Tarjeta de Búsqueda y Selección de Homónimos
    # ----------------------------------------------------
    frame_busqueda = ttk.LabelFrame(ventana, text=" 1. Búsqueda y Selección del Socio ", padding=12)
    frame_busqueda.pack(fill="x", padx=18, pady=(2, 8))

    fila_input = ttk.Frame(frame_busqueda, style="Card.TFrame")
    fila_input.pack(fill="x")

    ttk.Label(fila_input, text="DNI o Nombre:", style="Card.TLabel", font=(FUENTE_PRINCIPAL, 9, "bold")).pack(side="left", padx=(0, 8))
    entry_busqueda = ttk.Entry(fila_input, width=24)
    entry_busqueda.pack(side="left", padx=(0, 8))

    # Panel dinámico de homónimos (permanece oculto hasta que haya más de 1 coincidencia)
    frame_homonimos = ttk.Frame(frame_busqueda, style="Card.TFrame")
    lbl_aviso_homonimos = ttk.Label(
        frame_homonimos,
        text="Seleccione al socio correspondiente de la lista:",
        style="Accent.Card.TLabel"
    )
    lbl_aviso_homonimos.pack(anchor="w", pady=(8, 4))

    combo_coincidencias = ttk.Combobox(frame_homonimos, state="readonly", width=52)
    combo_coincidencias.pack(fill="x", pady=(0, 4))

    frame_lista = ttk.Frame(frame_homonimos, style="Card.TFrame")
    frame_lista.pack(fill="x")

    scroll_lista = ttk.Scrollbar(frame_lista, orient="vertical")
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

    meses_nombres = [
        "01 - Enero", "02 - Febrero", "03 - Marzo", "04 - Abril",
        "05 - Mayo", "06 - Junio", "07 - Julio", "08 - Agosto",
        "09 - Septiembre", "10 - Octubre", "11 - Noviembre", "12 - Diciembre"
    ]
    hoy = date.today()
    mes_actual_idx = hoy.month - 1

    ttk.Label(frame_cobro, text="Mes a cobrar:", style="Card.TLabel").grid(row=0, column=0, padx=8, pady=6, sticky="e")
    combo_mes = ttk.Combobox(frame_cobro, values=meses_nombres, state="readonly", width=20)
    combo_mes.grid(row=0, column=1, padx=8, pady=6, sticky="w")
    combo_mes.current(mes_actual_idx)

    ttk.Label(frame_cobro, text="Año:", style="Card.TLabel").grid(row=1, column=0, padx=8, pady=6, sticky="e")
    entry_anio = ttk.Entry(frame_cobro, width=12)
    entry_anio.grid(row=1, column=1, padx=8, pady=6, sticky="w")
    entry_anio.insert(0, str(hoy.year))

    ttk.Label(frame_cobro, text="Fecha de pago (DD/MM/AAAA):", style="Card.TLabel").grid(row=2, column=0, padx=8, pady=6, sticky="e")
    entry_fecha_pago = ttk.Entry(frame_cobro, width=20)
    entry_fecha_pago.grid(row=2, column=1, padx=8, pady=6, sticky="w")
    entry_fecha_pago.insert(0, hoy.strftime("%d/%m/%Y"))

    ttk.Label(frame_cobro, text="Importe cobrado ($):", style="Card.TLabel").grid(row=3, column=0, padx=8, pady=6, sticky="e")
    entry_monto = ttk.Entry(frame_cobro, width=20)
    entry_monto.grid(row=3, column=1, padx=8, pady=6, sticky="w")

    def _al_cambiar_tema(tema):
        listbox_coincidencias.configure(
            bg=tema["listbox_bg"],
            fg=tema["listbox_fg"],
            selectbackground=tema["btn_hover_bg"]
        )
        if estado_busqueda["socio"] is not None:
            cargar_datos_de_socio(estado_busqueda["socio"])

    configurar_estilos_modernos(ventana, callback_tema=_al_cambiar_tema)

    # Función que carga automáticamente en pantalla los datos y el arancel del socio seleccionado
    def cargar_datos_de_socio(s):
        estado_busqueda["socio"] = s
        estado_actual = s.obtener_estado_cuota()
        tema = obtener_tema_actual()
        es_noche = tema["nombre"] == "nocturno"

        if estado_actual == "Al día":
            color = "#49b6ff" if es_noche else "#15803d"
        elif "Pendiente" in estado_actual:
            color = "#fbbf24" if es_noche else "#b45309"
        else:
            color = "#ff499e" if es_noche else "#be123c"

        arancel = s.obtener_arancel_actual()
        entry_monto.delete(0, tk.END)
        entry_monto.insert(0, f"{arancel:.2f}")

        info = (
            f"✔ Socio seleccionado: {s.nombre} {s.apellido} (DNI: {s.dni})\n"
            f"• Actividad: {s.clase} | Turno: {s.turno} | Arancel sugerido: ${arancel:,.2f}\n"
            f"• Estado actual: {estado_actual} (Último período: {s.periodo_abonado or 'Sin registro'})"
        )
        lbl_datos_socio.config(text=info, foreground=color, font=(FUENTE_PRINCIPAL, 9, "bold"))

    # Eventos al seleccionar un homónimo de la lista o del menú desplegable
    def al_seleccionar_de_listbox(event=None):
        seleccion = listbox_coincidencias.curselection()
        if not seleccion:
            return
        idx = seleccion[0]
        coincidencias = estado_busqueda["coincidencias"]
        if 0 <= idx < len(coincidencias):
            combo_coincidencias.current(idx)
            cargar_datos_de_socio(coincidencias[idx])

    def al_seleccionar_de_combo(event=None):
        idx = combo_coincidencias.current()
        coincidencias = estado_busqueda["coincidencias"]
        if 0 <= idx < len(coincidencias):
            listbox_coincidencias.selection_clear(0, tk.END)
            listbox_coincidencias.selection_set(idx)
            listbox_coincidencias.see(idx)
            cargar_datos_de_socio(coincidencias[idx])

    listbox_coincidencias.bind("<<ListboxSelect>>", al_seleccionar_de_listbox)
    combo_coincidencias.bind("<<ComboboxSelected>>", al_seleccionar_de_combo)

    # Aquí se maneja la búsqueda contemplando 0, 1 o múltiples coincidencias (homónimos)
    def buscar(event=None):
        criterio = entry_busqueda.get().strip()
        if not criterio:
            messagebox.showwarning("Atención", "Escriba un DNI o Nombre para buscar.", parent=ventana)
            return

        socios = cargar_socios()
        coincidencias = buscar_socios_coincidentes(criterio, socios)
        estado_busqueda["coincidencias"] = coincidencias

        listbox_coincidencias.delete(0, tk.END)
        combo_coincidencias.set("")
        combo_coincidencias.config(values=[])

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

        opciones_formateadas = [
            f"{s.nombre} {s.apellido} - DNI: {s.dni} - {s.clase} ({s.turno})"
            for s in coincidencias
        ]
        combo_coincidencias.config(values=opciones_formateadas)
        for texto_op in opciones_formateadas:
            listbox_coincidencias.insert(tk.END, texto_op)

        if len(coincidencias) == 1:
            frame_homonimos.pack_forget()
            cargar_datos_de_socio(coincidencias[0])
        else:
            estado_busqueda["socio"] = None
            entry_monto.delete(0, tk.END)
            lbl_aviso_homonimos.config(
                text=f"🔎 Se encontraron {len(coincidencias)} coincidencias para '{criterio}'. Haga clic en el socio correcto:"
            )
            frame_homonimos.pack(fill="x", before=lbl_datos_socio)
            lbl_datos_socio.config(
                text="⚠️ Múltiples socios encontrados. Seleccione uno de la lista superior para cargar su arancel.",
                foreground="#d264b6",
                font=(FUENTE_PRINCIPAL, 9, "italic")
            )

    btn_buscar = ttk.Button(fila_input, text="🔍 Buscar Socio", command=buscar)
    btn_buscar.pack(side="left")
    entry_busqueda.bind("<Return>", buscar)

    # Aquí se maneja lo que pasa al hacer clic en "💳 Confirmar y Cobrar Cuota":
    def registrar_pago():
        s = estado_busqueda["socio"]
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

        fecha_pago_texto = entry_fecha_pago.get().strip()
        anio_texto = entry_anio.get().strip()
        monto_texto = entry_monto.get().strip().replace(",", ".")

        if not fecha_pago_texto or not anio_texto or not monto_texto:
            messagebox.showwarning("Atención", "Complete todos los campos del cobro.", parent=ventana)
            return

        try:
            datetime.strptime(fecha_pago_texto, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Error", "La fecha de pago debe tener formato DD/MM/AAAA.", parent=ventana)
            return

        if not anio_texto.isdigit() or len(anio_texto) != 4:
            messagebox.showerror("Error", "El año debe contener 4 dígitos (ej: 2026).", parent=ventana)
            return

        try:
            monto_cobrado = float(monto_texto)
            if monto_cobrado <= 0:
                messagebox.showerror("Error", "El importe debe ser mayor a cero.", parent=ventana)
                return
        except ValueError:
            messagebox.showerror("Error", "El importe debe ser un número válido.", parent=ventana)
            return

        socios = cargar_socios()
        socio_a_actualizar = None
        for item in socios:
            if item.dni == s.dni:
                socio_a_actualizar = item
                break

        if not socio_a_actualizar:
            messagebox.showerror("Error", "Error al recuperar los datos del socio.", parent=ventana)
            return

        mes_num = combo_mes.current() + 1
        periodo_formateado = f"{mes_num:02d}/{anio_texto}"

        socio_a_actualizar.registrar_pago(
            periodo=periodo_formateado,
            fecha_pago=fecha_pago_texto,
            monto=monto_cobrado
        )
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

        if callback_actualizar:
            callback_actualizar()
        ventana.destroy()

    frame_botones = ttk.Frame(frame_cobro, style="Card.TFrame")
    frame_botones.grid(row=4, column=0, columnspan=2, pady=(16, 4))

    btn_registrar = ttk.Button(frame_botones, text="💳 Confirmar y Cobrar Cuota", command=registrar_pago)
    btn_registrar.pack(side="left", padx=6)

    btn_cancelar = ttk.Button(frame_botones, text="Cancelar", command=ventana.destroy)
    btn_cancelar.pack(side="left", padx=6)


# ==============================================================================
# SECCIÓN 7: PANEL DE ESTADÍSTICAS, TABLA Y REPORTES PDF (pantalla_estadisticas.py)
# ==============================================================================
"""
1. PROPÓSITO GENERAL DE ESTA SECCIÓN:
   Muestra las métricas del club, la recaudación mensual, el buscador en vivo,
   los filtros rápidos, la tabla 'Treeview' con selección múltiple, la edición
   y eliminación de alumnos y la exportación de los reportes en PDF.
"""


def abrir_pantalla_estadisticas(root, callback_actualizar=None):
    """
    Construye y muestra el panel general de consultas, tabla interactiva y reportes PDF.
    """
    ventana = tk.Toplevel(root)
    ventana.title("Panel de Consultas, Gestión de Alumnos y Reportes - Sistema Náutico")
    ventana.geometry("960x680")
    ventana.minsize(850, 590)

    configurar_estilos_modernos(ventana)
    crear_boton_tema(ventana, padx=16, pady=(8, 2))

    # 1. Tarjeta de Resumen de Métricas e Ingresos por Mes
    frame_kpi = ttk.LabelFrame(ventana, text=" 📊 Resumen del Club y Recaudación Mensual ", padding=10)
    frame_kpi.pack(fill="x", padx=16, pady=4)

    lbl_kpi_alumnos = ttk.Label(frame_kpi, text="", style="Card.TLabel")
    lbl_kpi_alumnos.pack(anchor="w", pady=1)

    lbl_kpi_turnos = ttk.Label(frame_kpi, text="", style="Card.TLabel")
    lbl_kpi_turnos.pack(anchor="w", pady=1)

    lbl_kpi_dinero = ttk.Label(frame_kpi, text="", style="Accent.Card.TLabel")
    lbl_kpi_dinero.pack(anchor="w", pady=(3, 0))

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

    # 2. Tarjeta de Búsqueda en Vivo y Filtros Rápidos
    frame_filtros = ttk.LabelFrame(ventana, text=" 🔍 Búsqueda y Filtros ", padding=8)
    frame_filtros.pack(fill="x", padx=16, pady=4)

    ttk.Label(frame_filtros, text="Buscar (DNI o Nombre):", style="Card.TLabel").pack(side="left", padx=(4, 4))
    entry_busqueda = ttk.Entry(frame_filtros, width=20)
    entry_busqueda.pack(side="left", padx=(0, 12))

    ttk.Label(frame_filtros, text="Filtrar por:", style="Card.TLabel").pack(side="left", padx=(4, 4))
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

    # 3. Tarjeta de Tabla Interactiva (ttk.Treeview) y Acciones
    frame_panel_tabla = ttk.LabelFrame(ventana, text=" 📋 Nómina de Alumnos y Acciones ", padding=10)
    frame_panel_tabla.pack(fill="both", expand=True, padx=16, pady=(4, 14))

    frame_tabla = ttk.Frame(frame_panel_tabla, style="Card.TFrame")
    frame_tabla.pack(fill="both", expand=True, pady=(0, 6))

    columnas = ("dni", "nombre", "clase", "turno", "estado_cuota", "periodo", "apto", "estado")
    tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=11, selectmode="extended")

    tabla.heading("dni", text="DNI")
    tabla.heading("nombre", text="Apellido y Nombre")
    tabla.heading("clase", text="Actividad")
    tabla.heading("turno", text="Turno")
    tabla.heading("estado_cuota", text="Estado Cuota")
    tabla.heading("periodo", text="Período")
    tabla.heading("apto", text="Apto Médico")
    tabla.heading("estado", text="Estado")

    tabla.column("dni", width=80, anchor="center")
    tabla.column("nombre", width=180, anchor="w")
    tabla.column("clase", width=95, anchor="center")
    tabla.column("turno", width=80, anchor="center")
    tabla.column("estado_cuota", width=145, anchor="center")
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

    # 4. Operaciones sobre Alumnos: Modificar y Borrado Múltiple
    frame_gestion = ttk.Frame(frame_panel_tabla, style="Card.TFrame")
    frame_gestion.pack(fill="x", pady=4)

    def obtener_socios_seleccionados():
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

    def modificar_alumno():
        seleccionados = obtener_socios_seleccionados()
        if not seleccionados:
            return
        if len(seleccionados) > 1:
            messagebox.showinfo("Modificación Individual", "Para modificar datos, por favor seleccione un único alumno a la vez.", parent=ventana)
            return

        socio = seleccionados[0]
        def refrescar_todo():
            cargar_datos_tabla()
            if callback_actualizar:
                callback_actualizar()
        abrir_pantalla_edicion(ventana, socio, callback_actualizar=refrescar_todo)

    def eliminar_alumnos_seleccionados():
        seleccionados = obtener_socios_seleccionados()
        if not seleccionados:
            return

        cant = len(seleccionados)
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

        confirmado = messagebox.askyesno(titulo_alerta, pregunta, parent=ventana)
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

    def seleccionar_todos():
        tabla.selection_set(tabla.get_children())

    def deseleccionar_todos():
        tabla.selection_remove(tabla.selection())

    ttk.Button(frame_gestion, text="✏️ Modificar Alumno", command=modificar_alumno).pack(side="left", padx=4)
    ttk.Button(frame_gestion, text="🗑️ Eliminar Alumno(s) Seleccionado(s)", command=eliminar_alumnos_seleccionados).pack(side="left", padx=4)
    ttk.Button(frame_gestion, text="☑️ Seleccionar Todos", command=seleccionar_todos).pack(side="left", padx=4)
    ttk.Button(frame_gestion, text="⬜ Deseleccionar", command=deseleccionar_todos).pack(side="left", padx=4)

    ttk.Label(
        frame_gestion,
        text="(Ctrl + Clic o Shift + Clic para seleccionar múltiples)",
        style="Muted.Card.TLabel"
    ).pack(side="left", padx=8)

    tabla.bind("<Double-1>", lambda event: modificar_alumno())
    cargar_datos_tabla()

    # 5. Botones de Exportación PDF y Cierre
    frame_acciones = ttk.Frame(frame_panel_tabla, style="Card.TFrame")
    frame_acciones.pack(fill="x", pady=(6, 0))

    def exportar_general():
        socios = cargar_socios()
        if not socios:
            messagebox.showwarning("Atención", "No hay datos de socios para exportar.", parent=ventana)
            return
        ruta = generar_reporte_pdf(socios)
        messagebox.showinfo("Reporte Generado con Éxito", f"El Reporte General en PDF se guardó en:\n{ruta}", parent=ventana)
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
        messagebox.showinfo("Listado de Cobranzas Generado", f"El Listado de Avisos y Cobranzas se guardó en:\n{ruta}", parent=ventana)
        try:
            os.startfile(ruta)
        except Exception:
            pass

    ttk.Button(frame_acciones, text="📄 Descargar Reporte General (PDF)", command=exportar_general).pack(side="left", padx=4)
    ttk.Button(frame_acciones, text="⚠️ Descargar Listado de Cobranzas y Avisos (PDF)", command=exportar_avisos).pack(side="left", padx=4)
    ttk.Button(frame_acciones, text="Cerrar", command=ventana.destroy).pack(side="right", padx=4)


# ==============================================================================
# SECCIÓN 8: VENTANA PRINCIPAL E INICIO DEL SISTEMA (main.py)
# ==============================================================================
"""
1. PROPÓSITO GENERAL DE ESTA SECCIÓN:
   Construye la ventana principal ('root'), la barra de menús desplegables,
   el botón 🌙 / ☀️, la tarjeta de resumen en vivo y los 4 botones de acceso rápido.
"""


def iniciar_aplicacion():
    # Aquí se crea la ventana principal del programa
    root = tk.Tk()
    root.title("Sistema Náutico - Gestión de Alumnos y Cuotas")
    root.geometry("540x550")
    root.minsize(500, 520)

    # Aplicamos el motor visual y registramos 'actualizar_resumen' para cuando cambie entre Día y Noche
    configurar_estilos_modernos(root, callback_tema=lambda _tema: actualizar_resumen())

    # Barra de Menús Desplegables Superior (tk.Menu)
    menu_bar = tk.Menu(root, font=(FUENTE_PRINCIPAL, 9))
    root.config(menu=menu_bar)

    menu_socios = tk.Menu(menu_bar, tearoff=0, font=(FUENTE_PRINCIPAL, 9))
    menu_socios.add_command(label="Nuevo Alumno / Socio...", command=lambda: abrir_pantalla_clientes(root, actualizar_resumen))
    menu_socios.add_command(label="Consultar, Modificar o Eliminar Alumnos...", command=lambda: abrir_pantalla_estadisticas(root, actualizar_resumen))
    menu_bar.add_cascade(label="Alumnos", menu=menu_socios)

    menu_cobranzas = tk.Menu(menu_bar, tearoff=0, font=(FUENTE_PRINCIPAL, 9))
    menu_cobranzas.add_command(label="Registrar Cobro de Cuota...", command=lambda: abrir_pantalla_renovacion(root, actualizar_resumen))
    menu_cobranzas.add_command(label="Modificar Importes de Cuotas...", command=lambda: abrir_pantalla_precios(root, actualizar_resumen))
    menu_bar.add_cascade(label="Cobranzas", menu=menu_cobranzas)

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

    menu_reportes = tk.Menu(menu_bar, tearoff=0, font=(FUENTE_PRINCIPAL, 9))
    menu_reportes.add_command(label="Panel de Estadísticas y Tabla", command=lambda: abrir_pantalla_estadisticas(root, actualizar_resumen))
    menu_reportes.add_separator()
    menu_reportes.add_command(label="Exportar Reporte General (PDF)", command=lambda: exportar_pdf_directo("general"))
    menu_reportes.add_command(label="Exportar Listado de Avisos / Cobranza (PDF)", command=lambda: exportar_pdf_directo("avisos"))
    menu_bar.add_cascade(label="Reportes", menu=menu_reportes)

    def salir_programa():
        if messagebox.askyesno("Confirmar Salida", "¿Desea cerrar el sistema náutico?"):
            root.destroy()

    menu_sistema = tk.Menu(menu_bar, tearoff=0, font=(FUENTE_PRINCIPAL, 9))
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

    # Botón conmutador de Modo Día / Modo Noche arriba a la derecha
    crear_boton_tema(root, padx=35, pady=(10, 0))

    # Título principal del Dashboard
    ttk.Label(
        root,
        text="ESCUELA NÁUTICA\nKAYAK & NATACIÓN",
        style="Header.TLabel",
        justify="center"
    ).pack(pady=(4, 10))

    # Tarjeta de Resumen en Vivo al Iniciar
    frame_bienvenida = ttk.LabelFrame(root, text=" ✨ Estado del Club al Iniciar ", padding=12)
    frame_bienvenida.pack(fill="x", padx=35, pady=6)

    lbl_resumen_socios = ttk.Label(frame_bienvenida, text="", style="Card.TLabel")
    lbl_resumen_socios.pack(anchor="w")

    lbl_resumen_ingresos = ttk.Label(
        frame_bienvenida,
        text="",
        style="Accent.Card.TLabel"
    )
    lbl_resumen_ingresos.pack(anchor="w", pady=(4, 2))

    lbl_resumen_cuotas = ttk.Label(frame_bienvenida, text="", style="Card.TLabel", font=(FUENTE_PRINCIPAL, 9, "bold"))
    lbl_resumen_cuotas.pack(anchor="w", pady=(2, 0))

    def actualizar_resumen():
        socios = cargar_socios()
        stats = calcular_estadisticas(socios)
        hoy = date.today()
        periodo_actual = f"{hoy.month:02d}/{hoy.year}"
        recaudacion = calcular_recaudacion_mes(periodo=periodo_actual, socios=socios)
        tema = obtener_tema_actual()
        es_noche = tema["nombre"] == "nocturno"

        lbl_resumen_socios.config(
            text=f"Fecha: {hoy.strftime('%d/%m/%Y')} | Alumnos: {stats['total']}  "
                 f"(Kayak: {stats['kayak']}, Natación: {stats['natacion']}, Ambas: {stats['ambas']})"
        )

        lbl_resumen_ingresos.config(
            text=f"💵 Ingresos en cuotas ({periodo_actual}): ${recaudacion['total_recaudado']:,.2f} ({recaudacion['cantidad_pagos']} cobros)"
        )

        if hoy.day <= 10:
            texto_cuota = f"⚠️ {stats['pendientes']} alumnos pendientes de pago (Vencimiento regular: día 10)"
            color_cuota = "#fbbf24" if es_noche else "#b45309"
        else:
            texto_cuota = f"🚨 {stats['atrasados']} alumnos con cuota vencida (Pasó el día 10)"
            color_cuota = "#ff499e" if es_noche else "#be123c"

        if stats["total"] > 0 and stats["al_dia"] == stats["total"]:
            texto_cuota = "✅ ¡Todos los alumnos están al día este mes!"
            color_cuota = "#49b6ff" if es_noche else "#15803d"

        lbl_resumen_cuotas.config(text=texto_cuota, foreground=color_cuota)

    actualizar_resumen()

    # Botonera de Accesos Rápidos con efecto Hover y Clic
    ttk.Label(
        root,
        text="Accesos Rápidos del Panel:",
        style="SubHeader.TLabel"
    ).pack(anchor="w", padx=35, pady=(12, 4))

    ttk.Button(
        root,
        text="➕ Registrar Nuevo Alumno",
        command=lambda: abrir_pantalla_clientes(root, actualizar_resumen)
    ).pack(fill="x", padx=35, pady=4)

    ttk.Button(
        root,
        text="💳 Registrar Cobro de Cuota",
        command=lambda: abrir_pantalla_renovacion(root, actualizar_resumen)
    ).pack(fill="x", padx=35, pady=4)

    ttk.Button(
        root,
        text="💲 Modificar Importes de Cuotas",
        command=lambda: abrir_pantalla_precios(root, actualizar_resumen)
    ).pack(fill="x", padx=35, pady=4)

    ttk.Button(
        root,
        text="📊 Consultar, Modificar Alumnos y Recaudación",
        command=lambda: abrir_pantalla_estadisticas(root, actualizar_resumen)
    ).pack(fill="x", padx=35, pady=4)

    root.protocol("WM_DELETE_WINDOW", salir_programa)
    root.mainloop()


# Punto de arranque cuando se ejecuta directamente 'python entrega_final.py'
if __name__ == "__main__":
    iniciar_aplicacion()

