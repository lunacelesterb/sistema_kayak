import tkinter as tk
from tkinter import ttk, messagebox
from logica import cargar_socios, generar_reporte_pdf

def abrir(root):
    socios = cargar_socios()
    if not socios:
        messagebox.showwarning("Aviso", "No hay datos de socios para exportar")
        return
        
    ruta = generar_reporte_pdf(socios)
    messagebox.showinfo("Éxito", f"Reporte generado exitosamente en:\n{ruta}")