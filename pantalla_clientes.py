import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

from logica import (
    VALOR_SEGURO,
    calcular_vencimiento,
    certificado_es_obligatorio,
    determinar_actividad,
)

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


def abrir_pantalla_clientes(ventana_principal, clientes, guardar_datos):
    """Abre la pantalla de registro de clientes."""
    ventana = tk.Toplevel(ventana_principal)
    ventana.title("Registrar cliente")
    ventana.geometry("550x600")
    ventana.resizable(False, False)

    nombre = tk.StringVar()
    apellido = tk.StringVar()
    dni = tk.StringVar()
    telefono = tk.StringVar()
    mes = tk.StringVar()

    seguro_pagado = tk.BooleanVar()
    certificado_presentado = tk.BooleanVar()

    tk.Label(
        ventana, text="Registro de cliente", font=("Arial", 18, "bold")
    ).pack(pady=15)

    marco = tk.LabelFrame(
        ventana, text="Datos personales", padx=15, pady=15
    )
    marco.pack(padx=20, pady=10, fill="x")

    tk.Label(marco, text="Nombre:").grid(row=0, column=0, sticky="e", pady=5)
    tk.Entry(marco, textvariable=nombre, width=35).grid(
        row=0, column=1, pady=5
    )

    tk.Label(marco, text="Apellido:").grid(row=1, column=0, sticky="e", pady=5)
    tk.Entry(marco, textvariable=apellido, width=35).grid(
        row=1, column=1, pady=5
    )

    tk.Label(marco, text="DNI:").grid(row=2, column=0, sticky="e", pady=5)
    tk.Entry(marco, textvariable=dni, width=35).grid(row=2, column=1, pady=5)

    tk.Label(marco, text="Teléfono:").grid(row=3, column=0, sticky="e", pady=5)
    tk.Entry(marco, textvariable=telefono, width=35).grid(
        row=3, column=1, pady=5
    )

    tk.Label(marco, text="Mes de inscripción:").grid(
        row=4, column=0, sticky="e", pady=5
    )

    combo_mes = ttk.Combobox(
        marco,
        values=MESES,
        textvariable=mes,
        state="readonly",
        width=32,
    )
    combo_mes.grid(row=4, column=1, pady=5)

    etiqueta_actividad = tk.Label(
        marco, text="Seleccione un mes", font=("Arial", 10, "bold")
    )
    etiqueta_actividad.grid(row=5, column=0, columnspan=2, pady=15)

    def actualizar_actividad(event=None):
        if mes.get() == "":
            return

        actividad = determinar_actividad(mes.get())

        if certificado_es_obligatorio(mes.get()):
            texto = f"Actividad: {actividad}\nCertificado: Obligatorio"
            color = "darkblue"
        else:
            texto = f"Actividad: {actividad}\nCertificado: No obligatorio"
            color = "darkgreen"

        etiqueta_actividad.config(text=texto, fg=color)

    combo_mes.bind("<<ComboboxSelected>>", actualizar_actividad)

    tk.Checkbutton(
        marco, text="Seguro pagado", variable=seguro_pagado
    ).grid(row=6, column=0, columnspan=2, pady=5)

    tk.Checkbutton(
        marco,
        text="Certificado presentado",
        variable=certificado_presentado,
    ).grid(row=7, column=0, columnspan=2, pady=5)

    def registrar():
        if (
            nombre.get().strip() == ""
            or apellido.get().strip() == ""
            or dni.get().strip() == ""
            or mes.get() == ""
        ):
            messagebox.showwarning(
                "Datos incompletos", "Complete los campos obligatorios."
            )
            return

        for cliente in clientes:
            if cliente["dni"] == dni.get().strip():
                messagebox.showwarning(
                    "DNI repetido", "Ya existe un cliente con ese DNI."
                )
                return

        actividad = determinar_actividad(mes.get())

        if actividad == "Natación":
            certificado = (
                "Presentado" if certificado_presentado.get() else "Pendiente"
            )
        else:
            certificado = "No corresponde"

        fecha_pago = ""
        vencimiento = ""

        if seguro_pagado.get():
            hoy = date.today()
            fecha_pago = hoy.strftime("%d/%m/%Y")
            vencimiento = calcular_vencimiento(hoy).strftime("%d/%m/%Y")

        cliente = {
            "nombre": nombre.get().strip(),
            "apellido": apellido.get().strip(),
            "dni": dni.get().strip(),
            "telefono": telefono.get().strip(),
            "mes_inscripcion": mes.get(),
            "actividad": actividad,
            "certificado": certificado,
            "valor_seguro": VALOR_SEGURO,
            "fecha_pago_seguro": fecha_pago,
            "vencimiento_seguro": vencimiento,
        }

        clientes.append(cliente)
        guardar_datos(clientes)

        messagebox.showinfo(
            "Registro exitoso", "El cliente fue registrado correctamente."
        )
        ventana.destroy()

    tk.Button(
        ventana,
        text="Guardar cliente",
        width=25,
        bg="lightgreen",
        command=registrar,
    ).pack(pady=20)