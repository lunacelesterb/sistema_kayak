import tkinter as tk
from tkinter import ttk
import pantalla_clientes
import pantalla_renovacion
import pantalla_estadisticas

root = tk.Tk()
root.title("Sistema Kayak - Panel Principal")
root.geometry("400x300")
root.configure(bg="#f0f4f8")

estilo = ttk.Style()
estilo.theme_use("clam")

menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

# Menú Socios
menu_socios = tk.Menu(menu_bar, tearoff=0)
menu_socios.add_command(label="Nuevo Socio", command=lambda: pantalla_clientes.abrir(root))
menu_bar.add_cascade(label="Socios", menu=menu_socios)

# Menú Pagos
menu_pagos = tk.Menu(menu_bar, tearoff=0)
menu_pagos.add_command(label="Registrar Pago", command=lambda: pantalla_renovacion.abrir(root))
menu_bar.add_cascade(label="Pagos", menu=menu_pagos)

# Menú Reportes
menu_reportes = tk.Menu(menu_bar, tearoff=0)
menu_reportes.add_command(label="Generar PDF", command=lambda: pantalla_estadisticas.abrir(root))
menu_bar.add_cascade(label="Reportes", menu=menu_reportes)

# Menú Sistema
menu_sistema = tk.Menu(menu_bar, tearoff=0)
menu_sistema.add_command(label="Salir", command=root.destroy)
menu_bar.add_cascade(label="Sistema", menu=menu_sistema)

ttk.Label(root, text="SISTEMA KAYAK / NATACIÓN", font=("Segoe UI", 14, "bold"), background="#f0f4f8").pack(pady=25)

ttk.Button(root, text="Gestión de Socios", command=lambda: pantalla_clientes.abrir(root)).pack(fill="x", padx=60, pady=8)
ttk.Button(root, text="Control de Pagos", command=lambda: pantalla_renovacion.abrir(root)).pack(fill="x", padx=60, pady=8)
ttk.Button(root, text="Reportes PDF", command=lambda: pantalla_estadisticas.abrir(root)).pack(fill="x", padx=60, pady=8)

root.mainloop()