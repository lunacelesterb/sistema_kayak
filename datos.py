"""
================================================================================
ARCHIVO: datos.py (Modelo de Datos y Programación Orientada a Objetos - POO)
================================================================================

1. PROPÓSITO GENERAL:
   Este archivo es el "cerebro conceptual" del sistema. No dibuja ventanas ni botones,
   sino que le enseña a Python qué es una "Actividad" (Kayak, Natación o Ambas) y qué
   es un "Socio" (un alumno con DNI, nombre, apellido, fecha de nacimiento, turno,
   apto médico e historial de pagos). También se encarga de leer y guardar el archivo
   'precios.json' donde se almacenan los valores de las cuotas mensuales.

2. ELEMENTOS VISUALES / INTERFAZ:
   - Aunque no crea elementos gráficos directamente, este módulo genera los textos
     exactos que luego se muestran en las etiquetas y en la tabla visual de la interfaz:
     * "Al día" (cuando el socio ya pagó el mes actual).
     * "Pendiente (Vence el 10)" (del día 1 al 10 del mes si aún no pagó).
     * "Atrasado" (del día 11 en adelante si no registró el pago).

3. EXPLICACIÓN LÍNEA POR LÍNEA:
   Cada instrucción del código está comentada debajo en lenguaje sencillo para que
   puedas explicar exactamente qué hace y por qué está ahí durante tu defensa oral.
================================================================================
"""

# Aquí importamos 'os' para que Python sepa encontrar las carpetas y archivos en cualquier computadora
import os
# Aquí importamos 'json' para poder leer y guardar datos en archivos .json (nuestra base de datos)
import json
# Aquí importamos 'date' y 'datetime' para consultar la fecha real de hoy en el calendario de la PC
from datetime import date, datetime

# Aquí obtenemos la ruta exacta de la carpeta donde está guardado este archivo 'datos.py'
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
# Aquí unimos la carpeta actual con el nombre 'precios.json' para saber dónde buscar los precios
RUTA_PRECIOS = os.path.join(DIRECTORIO_ACTUAL, "precios.json")

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

    # ----------------------------------------------------
    # Métodos de Lógica de Negocio del Socio (POO)
    # ----------------------------------------------------
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

    # ----------------------------------------------------
    # Transformación a Diccionario para Guardar en JSON
    # ----------------------------------------------------
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
