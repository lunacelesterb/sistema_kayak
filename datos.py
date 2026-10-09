"""
Módulo de Datos - Sistema Kayak y Natación
Define las clases del modelo de objetos del sistema (POO):
- Actividad: Disciplinas (Kayak, Natación, Ambas) con sus aranceles y reglas.
- Socio: Datos del socio, actividad, turno (Mañana/Tarde), historial de pagos y apto médico.
"""
import os
import json
from datetime import date, datetime

DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RUTA_PRECIOS = os.path.join(DIRECTORIO_ACTUAL, "precios.json")

# Precios por defecto si todavía no existe el archivo de configuración
PRECIOS_PREDETERMINADOS = {
    "Kayak": 15000.0,
    "Natación": 18000.0,
    "Ambas": 28000.0
}


def cargar_precios():
    """
    Lee los precios de las cuotas desde 'precios.json'.
    Si no existe el archivo, lo crea con los valores predeterminados.
    """
    try:
        with open(RUTA_PRECIOS, "r", encoding="utf-8") as f:
            precios = json.load(f)
            # Asegurar que existan todas las claves
            for k, v in PRECIOS_PREDETERMINADOS.items():
                if k not in precios:
                    precios[k] = v
            return precios
    except (FileNotFoundError, json.JSONDecodeError):
        guardar_precios(PRECIOS_PREDETERMINADOS)
        return PRECIOS_PREDETERMINADOS.copy()


def guardar_precios(nuevos_precios):
    """
    Guarda los aranceles actualizados en 'precios.json'.
    Permite modificar los precios desde la interfaz en cualquier momento.
    """
    with open(RUTA_PRECIOS, "w", encoding="utf-8") as f:
        json.dump(nuevos_precios, f, indent=4, ensure_ascii=False)


class Actividad:
    """
    Clase que representa una disciplina deportiva disponible en el club.
    Puede ser 'Kayak', 'Natación' o 'Ambas' (Kayak + Natación).
    """
    def __init__(self, nombre, costo_mensual=None, requiere_apto=None):
        self.nombre = nombre
        precios = cargar_precios()
        
        # Si no se pasó un costo manual, se lee del archivo de precios configurados
        if costo_mensual is None:
            self.costo_mensual = float(precios.get(nombre, 15000.0))
        else:
            self.costo_mensual = float(costo_mensual)

        # Regla de seguridad: si practica Natación o Ambas, el certificado médico es obligatorio
        if requiere_apto is None:
            self.requiere_apto = nombre in ("Natación", "Ambas")
        else:
            self.requiere_apto = bool(requiere_apto)

    def to_dict(self):
        """Convierte los datos de la actividad a diccionario."""
        return {
            "nombre": self.nombre,
            "costo_mensual": self.costo_mensual,
            "requiere_apto": self.requiere_apto
        }

    def __str__(self):
        return f"{self.nombre} (${self.costo_mensual:,.2f})"


class Socio:
    """
    Clase que representa a un socio o alumno del club náutico.
    Contiene sus datos personales, turno, disciplina elegida y control de pagos.
    """
    def __init__(self, dni, nombre, apellido, fecha_de_nacimiento, clase="Kayak",
                 apto_medico=False, estado="Activo", cuota_al_dia=False,
                 mes_abonado="", dia_pago=0, periodo_abonado="", fecha_pago="",
                 turno="Mañana", historial_pagos=None, monto_ultimo_pago=0.0):
        # Datos personales
        self.dni = str(dni).strip()
        self.nombre = str(nombre).strip()
        self.apellido = str(apellido).strip()
        self.nacimiento = str(fecha_de_nacimiento).strip()
        
        # Turno al que asiste: 'Mañana' o 'Tarde'
        self.turno = str(turno).strip() if turno else "Mañana"

        # Relación con la clase Actividad
        if isinstance(clase, Actividad):
            self.actividad = clase
            self.clase = clase.nombre
        else:
            self.clase = str(clase)
            self.actividad = Actividad(self.clase)

        # Apto médico (obligatorio para Natación y Ambas)
        self.apto_medico = bool(apto_medico)
        self.estado = estado  # 'Activo' o 'Inactivo'

        # Datos del último pago
        self.periodo_abonado = periodo_abonado or mes_abonado
        self.fecha_pago = fecha_pago
        self.monto_ultimo_pago = float(monto_ultimo_pago) if monto_ultimo_pago else 0.0

        # Historial de todos los pagos realizados por el socio
        if historial_pagos is not None and isinstance(historial_pagos, list):
            self.historial_pagos = historial_pagos
        else:
            self.historial_pagos = []
            # Si ya tenía un pago registrado en el formato anterior, lo agregamos al historial
            if self.periodo_abonado:
                self.historial_pagos.append({
                    "periodo": self.periodo_abonado,
                    "fecha_pago": self.fecha_pago or "Histórico",
                    "monto": self.actividad.costo_mensual
                })

        # Campos de compatibilidad con versiones previas
        self.mes_abonado = mes_abonado or self.periodo_abonado
        self.dia_pago = dia_pago
        self.cuota_al_dia = cuota_al_dia

    # ----------------------------------------------------
    # Métodos de Lógica de Negocio (POO)
    # ----------------------------------------------------
    def obtener_arancel_actual(self):
        """Devuelve el costo actual de la cuota según la actividad elegida."""
        precios = cargar_precios()
        return float(precios.get(self.clase, self.actividad.costo_mensual))

    def obtener_periodo_actual(self, fecha_referencia=None):
        """Devuelve el período actual en formato 'MM/AAAA' (ej: '10/2026')."""
        ref = fecha_referencia or date.today()
        return f"{ref.month:02d}/{ref.year}"

    def tiene_mes_abonado(self, fecha_referencia=None):
        """
        Verifica si el socio tiene abonado el mes de la fecha indicada.
        Revisa tanto el último período como el historial de pagos.
        """
        ref = fecha_referencia or date.today()
        periodo_actual = self.obtener_periodo_actual(ref)

        meses_nombres = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        nombre_mes_actual = meses_nombres[ref.month - 1]

        # Verificar período principal
        p_actual = str(self.periodo_abonado).strip()
        if p_actual == periodo_actual or p_actual.lower() == nombre_mes_actual.lower():
            return True

        # Verificar en el historial de pagos
        for pago in self.historial_pagos:
            p = str(pago.get("periodo", "")).strip()
            if p == periodo_actual or p.lower() == nombre_mes_actual.lower():
                return True

        return False

    def obtener_estado_cuota(self, fecha_referencia=None):
        """
        Calcula dinámicamente el estado de la cuota según la fecha del día:
        - 'Al día': Abonó el período del mes corriente.
        - 'Pendiente (Vence el 10)': Es entre el día 1 y 10 y aún no pagó (para aviso).
        - 'Atrasado': Ya pasó el día 10 del mes y no tiene el pago registrado.
        """
        ref = fecha_referencia or date.today()

        if self.tiene_mes_abonado(ref):
            return "Al día"

        # Si aún no pagó el mes en curso, verificamos el día límite
        if ref.day <= 10:
            return "Pendiente (Vence el 10)"
        else:
            return "Atrasado"

    def esta_al_dia(self, fecha_referencia=None):
        """Devuelve True si el socio tiene la cuota del mes paga."""
        return self.obtener_estado_cuota(fecha_referencia) == "Al día"

    def necesita_aviso_cobro(self, fecha_referencia=None):
        """Devuelve True si el socio adeuda el mes actual."""
        return not self.tiene_mes_abonado(fecha_referencia)

    def tiene_apto_valido(self):
        """
        Verifica si cumple con el apto médico según su actividad.
        Si hace Kayak no requiere; si hace Natación o Ambas es obligatorio.
        """
        if self.actividad.requiere_apto:
            return self.apto_medico
        return True

    def esta_habilitado_para_ingreso(self, fecha_referencia=None):
        """
        Verifica si el alumno puede realizar la actividad en el agua:
        Requiere estar activo, apto médico presentado y no tener cuota atrasada.
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
        Registra el cobro de una cuota mensual:
        - Guarda el período y la fecha de pago.
        - Asigna el monto abonado.
        - Agrega el comprobante al historial de pagos del socio.
        """
        self.periodo_abonado = periodo
        self.mes_abonado = periodo
        self.fecha_pago = fecha_pago or date.today().strftime("%d/%m/%Y")
        
        arancel = float(monto) if monto is not None else self.obtener_arancel_actual()
        self.monto_ultimo_pago = arancel

        try:
            self.dia_pago = int(self.fecha_pago.split("/")[0])
        except (ValueError, IndexError):
            self.dia_pago = date.today().day

        # Registrar en el historial de pagos
        registro = {
            "periodo": periodo,
            "fecha_pago": self.fecha_pago,
            "monto": arancel
        }
        self.historial_pagos.append(registro)
        self.cuota_al_dia = self.esta_al_dia()

    # ----------------------------------------------------
    # Serialización a Diccionario (JSON)
    # ----------------------------------------------------
    def to_dict(self):
        """Convierte el objeto Socio en diccionario para persistir en JSON."""
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