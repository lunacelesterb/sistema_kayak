import tkinter as tk
from collections import Counter

MESES = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
]


def abrir_pantalla_estadisticas(ventana_principal, clientes):
    """Abre la pantalla de estadísticas."""
    ventana = tk.Toplevel(ventana_principal)
    ventana.title("Estadísticas")
    ventana.geometry("450x550")

    tk.Label(
        ventana, text="Estadísticas de inscriptos", font=("Arial", 18, "bold")
    ).pack(pady=20)

    if len(clientes) == 0:
        tk.Label(ventana, text="No hay clientes registrados.").pack(pady=20)
        return

    conteo = Counter(cliente["mes_inscripcion"] for cliente in clientes)
    total = len(clientes)

    for mes in MESES:
        cantidad = conteo[mes]
        if cantidad > 0:
            porcentaje = (cantidad / total) * 100
            texto = f"{mes}: {cantidad} cliente(s) - {porcentaje:.2f}%"
            tk.Label(ventana, text=texto, font=("Arial", 11)).pack(
                anchor="w", padx=40, pady=3
            )

    kayak = sum(cliente["actividad"] == "Kayak" for cliente in clientes)
    natacion = sum(cliente["actividad"] == "Natación" for cliente in clientes)

    tk.Label(
        ventana,
        text=f"\nTotal de clientes: {total}",
        font=("Arial", 11, "bold"),
    ).pack(pady=15)

    tk.Label(ventana, text=f"Clientes de kayak: {kayak}").pack()
    tk.Label(ventana, text=f"Clientes de natación: {natacion}").pack()