"""
Módulo de Lógica y Persistencia - Sistema Kayak y Natación
Gestiona la lectura y escritura de archivos JSON, cálculos estadísticos,
recaudación mensual de cuotas, búsquedas por DNI o Nombre, y reportes en PDF.
"""
import json
import os
from datetime import datetime, date
from fpdf import FPDF
from datos import Socio, cargar_precios, guardar_precios

# Configuración de rutas seguras basadas en la ubicación del script
DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RUTA_JSON = os.path.join(DIRECTORIO_ACTUAL, "clientes.json")
RUTA_PDF_GENERAL = os.path.join(DIRECTORIO_ACTUAL, "reporte_socios.pdf")
RUTA_PDF_AVISOS = os.path.join(DIRECTORIO_ACTUAL, "reporte_avisos_cobro.pdf")


# ----------------------------------------------------
# Persistencia de Datos en JSON
# ----------------------------------------------------
def cargar_socios():
    """
    Lee 'clientes.json' y reconstruye la lista de objetos Socio.
    Garantiza compatibilidad y control de errores si el archivo no existe o está vacío.
    """
    try:
        with open(RUTA_JSON, "r", encoding="utf-8") as f:
            datos = json.load(f)
            return [Socio(**d) for d in datos]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def guardar_socios(socios):
    """
    Guarda la lista completa de objetos Socio en 'clientes.json'.
    Conserva caracteres especiales (tildes, eñes) con 'ensure_ascii=False'.
    """
    with open(RUTA_JSON, "w", encoding="utf-8") as f:
        json.dump([s.to_dict() for s in socios], f, indent=4, ensure_ascii=False)


# ----------------------------------------------------
# Búsquedas y Consultas de Negocio
# ----------------------------------------------------
def buscar_socio(criterio, socios=None):
    """
    Busca un socio por DNI exacto o por coincidencia en Nombre y Apellido.
    Devuelve el primer Socio coincidente o None.
    """
    lista = socios if socios is not None else cargar_socios()
    texto = str(criterio).strip().lower()

    # 1. Búsqueda exacta por DNI
    for s in lista:
        if s.dni.lower() == texto:
            return s

    # 2. Búsqueda por Nombre o Apellido
    for s in lista:
        nombre_completo = f"{s.nombre} {s.apellido}".lower()
        if texto in s.nombre.lower() or texto in s.apellido.lower() or texto in nombre_completo:
            return s

    return None


def eliminar_socio(dni, socios=None):
    """
    Elimina al socio con el DNI indicado de la lista y guarda los cambios en JSON.
    Devuelve True si se eliminó con éxito, False si no se encontró.
    """
    lista = socios if socios is not None else cargar_socios()
    dni_limpio = str(dni).strip()
    nueva_lista = [s for s in lista if s.dni != dni_limpio]

    if len(nueva_lista) < len(lista):
        guardar_socios(nueva_lista)
        return True
    return False


def actualizar_socio(dni_original, datos_actualizados):
    """
    Actualiza los datos personales, actividad, turno o apto de un socio existente.
    Guarda los cambios persistidos en el archivo JSON.
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
    Filtra la lista de socios combinando búsqueda por texto (DNI, Nombre o Apellido)
    y filtro por estado de cuota o apto médico.
    """
    lista = socios if socios is not None else cargar_socios()
    resultado = []
    t = texto_busqueda.strip().lower()

    for s in lista:
        # Filtro de texto
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

        # Filtro de categoría / estado
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


def calcular_recaudacion_mes(periodo=None, socios=None):
    """
    Calcula el total de dinero recaudado en concepto de cuotas para un período (ej: '10/2026').
    Si no se especifica período, toma el mes actual.
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
            # Si el período coincide (ej. '10/2026' o 'Octubre')
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
    Calcula métricas globales del club para presentar en pantalla:
    - Total socios, distribución por actividad (Kayak / Natación / Ambas) y turnos.
    - Situación de cuotas y recaudación del mes en curso.
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
# Generación de Reportes PDF con fpdf2
# ----------------------------------------------------
def generar_reporte_pdf(socios, ruta_destino=RUTA_PDF_GENERAL):
    """
    Genera un informe completo en PDF con todos los socios registrados,
    sus datos personales, turno, actividad, arancel, apto y estado de cuota.
    """
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Encabezado institucional
    pdf.set_font("Helvetica", style="B", size=15)
    pdf.cell(0, 9, "SISTEMA NÁUTICO - REPORTE GENERAL DE SOCIOS", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", size=9)
    fecha_emision = datetime.now().strftime("%d/%m/%Y %H:%M")
    pdf.cell(0, 5, f"Fecha de emisión: {fecha_emision} | Día límite de cuota regular: 10 de cada mes", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # Cabecera de la tabla
    pdf.set_font("Helvetica", style="B", size=8)
    pdf.set_fill_color(220, 230, 245)

    anchos = [22, 54, 22, 28, 20, 24, 26, 26, 38]
    columnas = ["DNI", "Apellido y Nombre", "F. Nac.", "Actividad", "Turno", "Apto Méd.", "Período", "F. Pago", "Estado Cuota"]

    for i, col in enumerate(columnas):
        pdf.cell(anchos[i], 7, col, border=1, align="C", fill=True)
    pdf.ln()

    # Filas con los socios
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

    # Resumen y métricas al pie del reporte
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
    Genera el informe enfocado en cobranzas y avisos a socios:
    Lista los socios que aún adeudan la cuota del mes corriente.
    """
    pendientes = [s for s in socios if s.necesita_aviso_cobro()]

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Encabezado
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

    # Cabecera de la tabla
    pdf.set_font("Helvetica", style="B", size=9)
    pdf.set_fill_color(254, 237, 237)
    anchos = [25, 58, 28, 24, 28, 27]
    columnas = ["DNI", "Socio", "Actividad", "Turno", "Arancel", "Situación"]

    for i, col in enumerate(columnas):
        pdf.cell(anchos[i], 7, col, border=1, align="C", fill=True)
    pdf.ln()

    # Filas
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

        # Total pendiente
        pdf.ln(3)
        pdf.set_font("Helvetica", style="B", size=9)
        pdf.cell(0, 6, f"Total pendiente a cobrar: ${total_a_cobrar:,.2f} ({len(pendientes)} socios)", border="T", align="R")

    pdf.output(ruta_destino)
    return ruta_destino