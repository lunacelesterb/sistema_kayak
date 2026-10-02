import calendar
from datetime import date

VALOR_SEGURO = 40000
MESES_REEMPLAZO = ["Junio", "Julio", "Agosto"]


def determinar_actividad(mes):
    """Devuelve la actividad según el mes."""
    if mes in MESES_REEMPLAZO:
        return "Natación"
    return "Kayak"


def certificado_es_obligatorio(mes):
    """Indica si el certificado médico es obligatorio."""
    return mes in MESES_REEMPLAZO


def sumar_tres_meses(fecha):
    """Suma tres meses a una fecha."""
    nuevo_mes = fecha.month + 3
    nuevo_anio = fecha.year + (nuevo_mes - 1) // 12
    nuevo_mes = (nuevo_mes - 1) % 12 + 1

    ultimo_dia = calendar.monthrange(nuevo_anio, nuevo_mes)[1]
    nuevo_dia = min(fecha.day, ultimo_dia)

    return date(nuevo_anio, nuevo_mes, nuevo_dia)


def convertir_fecha(texto):
    """Convierte DD/MM/AAAA en un objeto de tipo date."""
    try:
        dia, mes, anio = texto.split("/")
        return date(int(anio), int(mes), int(dia))
    except Exception:
        return None


def calcular_vencimiento(fecha_pago):
    """Calcula el vencimiento del seguro a 3 meses."""
    return sumar_tres_meses(fecha_pago)


def obtener_estado_seguro(cliente):
    """Devuelve Pendiente, Vigente o Vencido."""
    vencimiento = cliente.get("vencimiento_seguro", "")

    if vencimiento == "":
        return "Pendiente"

    fecha_vencimiento = convertir_fecha(vencimiento)

    if fecha_vencimiento is None:
        return "Pendiente"

    if fecha_vencimiento >= date.today():
        return "Vigente"

    return "Vencido"