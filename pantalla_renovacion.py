import tkinter as tk
from tkinter import ttk, messagebox
from logica import cargar_socios, guardar_socios

def abrir(root):
    ventana = tk.Toplevel(root)
    ventana.title("Control de Pagos")
    ventana.geometry("350x200")

    ttk.Label(ventana, text="DNI del Socio:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_dni = ttk.Entry(ventana)
    entry_dni.grid(row=0, column=1, padx=10, pady=10)

    ttk.Label(ventana, text="Mes a abonar:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    combo_mes = ttk.Combobox(ventana, values=meses, state="readonly")
    combo_mes.grid(row=1, column=1, padx=10, pady=10)

    ttk.Label(ventana, text="Día de pago (1-31):").grid(row=2, column=0, padx=10, pady=10, sticky="e")
    entry_dia = ttk.Entry(ventana)
    entry_dia.grid(row=2, column=1, padx=10, pady=10)

    def registrar_pago():
        dni = entry_dni.get()
        mes = combo_mes.get()
        
        if not dni or not mes or not entry_dia.get():
            messagebox.showwarning("Error", "Completá todos los campos")
            return
            
        try:
            dia = int(entry_dia.get())
        except ValueError:
            messagebox.showerror("Error", "El día debe ser un número")
            return

        socios = cargar_socios()
        encontrado = False
        
        for s in socios:
            if s.dni == dni:
                s.mes_abonado = mes
                s.dia_pago = dia
                encontrado = True
                break
        
        if encontrado:
            guardar_socios(socios)
            estado = "Al día" if dia <= 10 else "Vencido"
            messagebox.showinfo("Éxito", f"Pago registrado.\nEstado de la cuota: {estado}")
            ventana.destroy()
        else:
            messagebox.showerror("Error", "Socio no encontrado")

    ttk.Button(ventana, text="Registrar Pago", command=registrar_pago).grid(row=3, column=0, columnspan=2, pady=10)