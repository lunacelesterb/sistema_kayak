"""
================================================================================
ARCHIVO: pantalla_precios.py (Configuración de Importes Mensuales de Cuotas)
================================================================================

1. PROPÓSITO GENERAL:
   Este módulo permite consultar y modificar el precio en pesos ($) de las cuotas
   mensuales de cada disciplina ("Kayak", "Natación" y "Ambas") directamente desde
   la interfaz gráfica, sin necesidad de modificar el código fuente. Al guardar,
   actualiza el archivo 'precios.json'.

2. ELEMENTOS VISUALES / INTERFAZ:
   - Ventana Secundaria ('ventana = tk.Toplevel'): Mide 430x360 píxeles, con tamaño
     fijo y fondo difuminado ('fondo.jpg').
   - Botón Conmutador de Tema (🌙 / ☀️): Ubicado arriba a la derecha.
   - Tarjeta ('frame = ttk.LabelFrame'): Cuadro con borde Azul Glicina (#779be7) que
     presenta las 3 cajas de texto ('ttk.Entry' de ancho 16) precargadas con los
     valores vigentes de cada actividad.
   - Botones ('💾 Guardar Cambios' y 'Cancelar'): Con efecto Hover en color Cielo
     Fresco (#49b6ff) y crecimiento de letra al hacer clic.

3. EXPLICACIÓN LÍNEA POR LÍNEA:
   Cada instrucción está comentada debajo en lenguaje claro para tu defensa oral.
================================================================================
"""

# Aquí importamos 'tkinter', 'ttk' y 'messagebox' para construir la ventana y mostrar avisos
import tkinter as tk
from tkinter import ttk, messagebox
# Aquí importamos las funciones que leen y guardan 'precios.json' desde 'datos.py'
from datos import cargar_precios, guardar_precios
# Aquí importamos el motor de estilos visuales y el botón de Modo Día / Modo Noche desde 'logica.py'
from logica import configurar_estilos_modernos, crear_boton_tema


def abrir(root, callback_actualizar=None):
    """
    Abre la ventana emergente para editar los importes mensuales de las cuotas.
    """
    # Aquí se crea la ventana emergente hija de 'root'
    ventana = tk.Toplevel(root)
    ventana.title("Configuración de Aranceles de Cuotas")
    # Aquí se define el tamaño de la ventana: 430 píxeles de ancho por 360 píxeles de alto
    ventana.geometry("430x360")
    ventana.resizable(False, False)
    ventana.grab_set()

    # Aquí aplicamos el fondo difuminado y los estilos de la paleta azul
    configurar_estilos_modernos(ventana)
    # Aquí colocamos el botón 🌙 / ☀️ arriba a la derecha
    crear_boton_tema(ventana, padx=18, pady=(10, 2))

    # Aquí creamos la tarjeta contenedora para los 3 campos de precios
    frame = ttk.LabelFrame(ventana, text=" 💲 Modificación de Importes Mensuales ($) ", padding=15)
    frame.pack(fill="both", expand=True, padx=18, pady=(4, 16))

    # Leemos los precios actuales guardados en 'precios.json'
    precios_actuales = cargar_precios()

    # --- FILA 0: Precio de Kayak ---
    ttk.Label(frame, text="Cuota Kayak ($):", style="Card.TLabel").grid(row=0, column=0, padx=10, pady=8, sticky="e")
    entry_kayak = ttk.Entry(frame, width=16)
    entry_kayak.grid(row=0, column=1, padx=10, pady=8, sticky="w")
    # '.insert(0, ...)' escribe dentro de la caja de texto el precio actual de Kayak
    entry_kayak.insert(0, str(precios_actuales.get("Kayak", 15000.0)))

    # --- FILA 1: Precio de Natación ---
    ttk.Label(frame, text="Cuota Natación ($):", style="Card.TLabel").grid(row=1, column=0, padx=10, pady=8, sticky="e")
    entry_natacion = ttk.Entry(frame, width=16)
    entry_natacion.grid(row=1, column=1, padx=10, pady=8, sticky="w")
    entry_natacion.insert(0, str(precios_actuales.get("Natación", 18000.0)))

    # --- FILA 2: Precio de Ambas Actividades (Combo) ---
    ttk.Label(frame, text="Cuota Ambas (Combo) ($):", style="Card.TLabel").grid(row=2, column=0, padx=10, pady=8, sticky="e")
    entry_ambas = ttk.Entry(frame, width=16)
    entry_ambas.grid(row=2, column=1, padx=10, pady=8, sticky="w")
    entry_ambas.insert(0, str(precios_actuales.get("Ambas", 28000.0)))

    # Aquí se maneja lo que pasa cuando el usuario hace clic en "💾 Guardar Cambios":
    def guardar():
        try:
            # Leemos los 3 textos, reemplazamos comas por puntos y los convertimos a números decimales (float)
            val_kayak = float(entry_kayak.get().strip().replace(",", "."))
            val_natacion = float(entry_natacion.get().strip().replace(",", "."))
            val_ambas = float(entry_ambas.get().strip().replace(",", "."))

            # Validamos que ningún precio sea cero ni negativo
            if val_kayak <= 0 or val_natacion <= 0 or val_ambas <= 0:
                messagebox.showerror("Error", "Los importes deben ser mayores a cero.", parent=ventana)
                return

            # Armamos el diccionario con los nuevos importes
            nuevos = {
                "Kayak": val_kayak,
                "Natación": val_natacion,
                "Ambas": val_ambas
            }
            # Guardamos los nuevos valores en el archivo 'precios.json'
            guardar_precios(nuevos)

            messagebox.showinfo(
                "Aranceles Actualizados",
                "Los nuevos importes fueron guardados exitosamente en 'precios.json'.\n"
                "Se aplicarán a los nuevos cobros.",
                parent=ventana
            )

            # Refrescamos la pantalla principal si corresponde y cerramos la ventana
            if callback_actualizar:
                callback_actualizar()

            ventana.destroy()

        # Si el usuario escribió letras o símbolos no numéricos, mostramos este mensaje de error
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos.", parent=ventana)

    # --- FILA 3: Botones de Guardar y Cancelar ---
    frame_botones = ttk.Frame(frame, style="Card.TFrame")
    frame_botones.grid(row=3, column=0, columnspan=2, pady=(16, 4))

    btn_guardar = ttk.Button(frame_botones, text="💾 Guardar Cambios", command=guardar)
    btn_guardar.pack(side="left", padx=6)

    btn_cancelar = ttk.Button(frame_botones, text="Cancelar", command=ventana.destroy)
    btn_cancelar.pack(side="left", padx=6)
