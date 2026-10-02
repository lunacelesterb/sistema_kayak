import tkinter as tk
from datetime import date
from tkinter import messagebox

from logica import VALOR_SEGURO, calcular_vencimiento, convertir_fecha


def abrir_pantalla_renovacion(ventana_principal, clientes, guardar_datos):
    """Abre la pantalla para renovar el seguro."""
    ventana = tk.Toplevel(ventana_principal)
    ventana.title("Renovar seguro")
    ventana.geometry("400x350")
    ventana.resizable(False, False)

    dni = tk.StringVar()

    tk.Label(
        ventana, text="Renovación de seguro", font=("Arial", 18, "bold")
    ).pack(pady=20)

    tk.Label(ventana, text="DNI del cliente:").pack(pady=5)
    tk.Entry(ventana, textvariable=dni, width=30).pack(pady=5)

    tk.Label(
        ventana,
        text="Importe: $40.000\nDuración: 3 meses",
        font=("Arial", 11),
    ).pack(pady=20)

    def renovar():
        dni_buscado = dni.get().strip()

        if dni_buscado == "":
            messagebox.showwarning("Dato faltante", "Ingrese el DNI.")
            return

        cliente_encontrado = None

        for cliente in clientes:
            if cliente["dni"] == dni_buscado:
                cliente_encontrado = cliente
                break

        if cliente_encontrado is None:
            messagebox.showerror(
                "Cliente inexistente", "No se encontró ese DNI."
            )
            return

        hoy = date.today()
        fecha_anterior = convertir_fecha(
            cliente_encontrado.get("vencimiento_seguro", "")
        )

        if fecha_anterior is not None and fecha_anterior >= hoy:
            nuevo_vencimiento = calcular_vencimiento(fecha_anterior)
        else:
            nuevo_vencimiento = calcular_vencimiento(hoy)

        cliente_encontrado["valor_seguro"] = VALOR_SEGURO
        cliente_encontrado["fecha_pago_seguro"] = hoy.strftime("%d/%m/%Y")
        cliente_encontrado["vencimiento_seguro"] = nuevo_vencimiento.strftime(
            "%d/%m/%Y"
        )

        guardar_datos(clientes)

        messagebox.showinfo(
            "Renovación exitosa",
            "El seguro fue renovado correctamente.\n"
            f"Nuevo vencimiento: {cliente_encontrado['vencimiento_seguro']}",
        )
        ventana.destroy()

    tk.Button(
        ventana, text="Registrar renovación", width=25, command=renovar
    ).pack(pady=15)