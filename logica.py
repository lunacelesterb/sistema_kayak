import json
import os
from fpdf import FPDF
from datos import Socio

DIRECTORIO_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RUTA_JSON = os.path.join(DIRECTORIO_ACTUAL, "clientes.json")
RUTA_PDF = os.path.join(DIRECTORIO_ACTUAL, "reporte_socios.pdf")

def cargar_socios():
    try:
        with open(RUTA_JSON, "r", encoding="utf-8") as f:
            datos = json.load(f)
            return [Socio(**d) for d in datos]
    except FileNotFoundError:
        return []

def guardar_socios(socios):
    with open(RUTA_JSON, "w", encoding="utf-8") as f:
        json.dump([s.to_dict() for s in socios], f, indent=4)

def generar_reporte_pdf(socios):
    pdf = FPDF(orientation="L")
    pdf.add_page()
    pdf.set_font("Helvetica", size=14)
    pdf.cell(0, 10, "Reporte Detallado de Socios", ln=True, align="C")
    pdf.set_font("Helvetica", size=9)
    
    pdf.cell(20, 10, "DNI", border=1)
    pdf.cell(60, 10, "Apellido y Nombre", border=1)
    pdf.cell(25, 10, "F. Nac", border=1)
    pdf.cell(30, 10, "Clase", border=1)
    pdf.cell(25, 10, "Apto Médico", border=1)
    pdf.cell(30, 10, "Mes Abonado", border=1)
    pdf.cell(30, 10, "Vencimiento", border=1, ln=True)

    for s in socios:
        if s.clase == "Natación":
            apto = "Sí" if s.apto_medico else "Falta"
        else:
            apto = "No requiere"

        vencimiento = "Impago"
        if s.mes_abonado:
            vencimiento = "Al día" if s.dia_pago <= 10 else "Vencido"

        nombre_completo = f"{s.apellido}, {s.nombre}"

        pdf.cell(20, 10, str(s.dni), border=1)
        pdf.cell(60, 10, nombre_completo, border=1)
        pdf.cell(25, 10, str(s.nacimiento), border=1)
        pdf.cell(30, 10, str(s.clase), border=1)
        pdf.cell(25, 10, apto, border=1)
        pdf.cell(30, 10, str(s.mes_abonado) if s.mes_abonado else "-", border=1)
        pdf.cell(30, 10, vencimiento, border=1, ln=True)
    
    pdf.output(RUTA_PDF)
    return RUTA_PDF