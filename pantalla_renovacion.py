"""
Módulo de Interfaz Gráfica - Control y Registro de Cobranzas
Permite buscar al socio por DNI o Nombre, visualizar su arancel correspondiente,
registrar el cobro con fecha real y alimentar el historial de ingresos mensuales.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime
from logica import cargar_socios, guardar_socios, buscar_socio


def abrir(root, callback_actualizar=None):
    """
    Abre la ventana para cobrar y registrar el pago de cuota de un socio.
    """
    ventana = tk.Toplevel(root)
    ventana.title("Registro de Cobro de Cuota - Sistema Náutico")
    ventana.geometry("480x470")
    ventana.resizable(False, False)
    ventana.grab_set()

    frame = ttk.Frame(ventana, padding=15)
    frame.pack(fill="both", expand=True)

    # 1. Búsqueda de Socio (DNI o Nombre)
    ttk.Label(frame, text="Buscar Socio (DNI o Nombre):").grid(row=0, column=0, padx=8, pady=6, sticky="e")
    entry_busqueda = ttk.Entry(frame, width=20)
    entry_busqueda.grid(row=0, column=1, padx=8, pady=6, sticky="w")

    socio_seleccionado = {"socio": None}

    # Tarjeta de datos del socio encontrado
    lbl_datos_socio = ttk.Label(
        frame,
        text="Ingrese DNI o Nombre y presione 'Buscar Socio'.",
        font=("Segoe UI", 9, "italic"),
        foreground="#555555"
    )
    lbl_datos_socio.grid(row=1, column=0, columnspan=2, padx=8, pady=8)

    # 2. Selección de Período (Mes y Año)
    meses_nombres = [
        "01 - Enero", "02 - Febrero", "03 - Marzo", "04 - Abril",
        "05 - Mayo", "06 - Junio", "07 - Julio", "08 - Agosto",
        "09 - Septiembre", "10 - Octubre", "11 - Noviembre", "12 - Diciembre"
    ]
    hoy = date.today()
    mes_actual_idx = hoy.month - 1

    ttk.Label(frame, text="Mes a cobrar:").grid(row=2, column=0, padx=8, pady=6, sticky="e")
    combo_mes = ttk.Combobox(frame, values=meses_nombres, state="readonly", width=18)
    combo_mes.grid(row=2, column=1, padx=8, pady=6, sticky="w")
    combo_mes.current(mes_actual_idx)

    ttk.Label(frame, text="Año:").grid(row=3, column=0, padx=8, pady=6, sticky="e")
    entry_anio = ttk.Entry(frame, width=12)
    entry_anio.grid(row=3, column=1, padx=8, pady=6, sticky="w")
    entry_anio.insert(0, str(hoy.year))

    # 3. Fecha real del cobro
    ttk.Label(frame, text="Fecha de pago (DD/MM/AAAA):").grid(row=4, column=0, padx=8, pady=6, sticky="e")
    entry_fecha_pago = ttk.Entry(frame, width=18)
    entry_fecha_pago.grid(row=4, column=1, padx=8, pady=6, sticky="w")
    entry_fecha_pago.insert(0, hoy.strftime("%d/%m/%Y"))

    # 4. Importe a cobrar ($)
    ttk.Label(frame, text="Importe cobrado ($):").grid(row=5, column=0, padx=8, pady=6, sticky="e")
    entry_monto = ttk.Entry(frame, width=18)
    entry_monto.grid(row=5, column=1, padx=8, pady=6, sticky="w")

    # Función de búsqueda
    def buscar():
        criterio = entry_busqueda.get().strip()
        if not criterio:
            messagebox.showwarning("Atención", "Escriba un DNI o Nombre para buscar.", parent=ventana)
            return

        socios = cargar_socios()
        s = buscar_socio(criterio, socios)

        if s is None:
            socio_seleccionado["socio"] = None
            entry_monto.delete(0, tk.END)
            lbl_datos_socio.config(
                text=f"❌ No se encontró ningún socio con '{criterio}'.",
                foreground="red"
            )
        else:
            socio_seleccionado["socio"] = s
            estado_actual = s.obtener_estado_cuota()
            color = "green" if estado_actual == "Al día" else ("orange" if "Pendiente" in estado_actual else "red")

            arancel = s.obtener_arancel_actual()
            entry_monto.delete(0, tk.END)
            entry_monto.insert(0, f"{arancel:.2f}")

            info = (
                f"Socio: {s.nombre} {s.apellido} (DNI: {s.dni})\n"
                f"Actividad: {s.clase} | Turno: {s.turno}\n"
                f"Estado actual: {estado_actual} (Último pago: {s.periodo_abonado or 'Sin registro'})"
            )
            lbl_datos_socio.config(text=info, foreground=color)

    btn_buscar = ttk.Button(frame, text="Buscar Socio", command=buscar)
    btn_buscar.grid(row=0, column=1, padx=(145, 0), sticky="w")

    # Registrar el cobro
    def registrar_pago():
        s = socio_seleccionado["socio"]
        if s is None:
            # Intentar buscar automáticamente con lo escrito
            buscar()
            s = socio_seleccionado["socio"]
            if s is None:
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
        # Encontrar la instancia en la lista completa para persistir
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

        # Registrar el pago con monto en el socio
        socio_a_actualizar.registrar_pago(
            periodo=periodo_formateado,
            fecha_pago=fecha_pago_texto,
            monto=monto_cobrado
        )

        guardar_socios(socios)

        nuevo_estado = socio_a_actualizar.obtener_estado_cuota()
        messagebox.showinfo(
            "Cobro Registrado con Éxito",
            f"Se registró el cobro para {socio_a_actualizar.nombre} {socio_a_actualizar.apellido}.\n\n"
            f"• Período abonado: {periodo_formateado}\n"
            f"• Fecha de cobro: {fecha_pago_texto}\n"
            f"• Importe ingresado: ${monto_cobrado:,.2f}\n"
            f"• Estado de cuota: {nuevo_estado}",
            parent=ventana
        )

        if callback_actualizar:
            callback_actualizar()

        ventana.destroy()

    frame_botones = ttk.Frame(frame)
    frame_botones.grid(row=6, column=0, columnspan=2, pady=20)

    btn_registrar = ttk.Button(frame_botones, text="Confirmar y Cobrar Cuota", command=registrar_pago)
    btn_registrar.pack(side="left", padx=5)

    btn_cancelar = ttk.Button(frame_botones, text="Cancelar", command=ventana.destroy)
    btn_cancelar.pack(side="left", padx=5)