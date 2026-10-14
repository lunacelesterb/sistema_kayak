# Sistema de Gestión Náutica (Kayak y Natación)

Trabajo Integrador Final (TIF) desarrollado en **Python** con interfaz gráfica **Tkinter / ttk**, persistencia en **JSON** y generación de reportes en PDF con **fpdf2**.

## 📌 Funcionalidades Principales

1. **Gestión de Alumnos / Socios:**
   - Alta de alumnos con validación de DNI numérico y formato de fecha (`DD/MM/AAAA`).
   - Selección de actividad (**Kayak**, **Natación** o **Ambas**).
   - Turnos asignados (**Mañana** y **Tarde**).
   - Control de Apto Médico: obligatorio para Natación y Ambas actividades.
   - **Modificación y Edición:** Posibilidad de editar los datos de cualquier alumno (nombre, apellido, fecha de nacimiento, actividad, turno, apto médico y estado Activo/Inactivo).
   - **Eliminación Individual y Múltiple:** Baja de alumnos (individual o en bloque seleccionando varios con Ctrl/Shift o el botón de seleccionar todos) con diálogo de confirmación detallado.

2. **Control Inteligente de Cuotas basado en Fechas:**
   - **Al día:** Cuota del mes corriente abonada.
   - **Pendiente (Vence el día 10):** Del día 1 al 10 del mes en curso para los socios que aún no pagaron. Permite emitir listados de recordatorio preventivo (por ejemplo, el día 9).
   - **Atrasado / Moroso:** A partir del día 11 si el socio no regularizó el pago.
   - Registro de cobro con fecha real y período mensual correspondiente.
   - Configuración de importes de aranceles desde la interfaz gráfica.

3. **Consultas, Recaudación y Métricas en Tiempo Real:**
   - Tabla interactiva (`ttk.Treeview`) para consultar todos los alumnos con buscador por DNI o Nombre.
   - Filtros rápidos: *Para avisar (Sin pago este mes)*, *Atrasados*, *Al día*, *Aptos pendientes* y por *Turno*.
   - Cálculo en tiempo real de la recaudación mensual en cuotas.
   - Resumen numérico en la ventana principal al iniciar el sistema.

4. **Reportes en PDF (`fpdf2`):**
   - **Reporte General:** Listado completo institucional con totales y estadísticas.
   - **Listado de Avisos y Cobranzas:** Reporte específico enfocado en los socios que adeudan el mes para gestionar recordatorios e intimaciones.

## 🧱 Arquitectura del Proyecto (POO)

- `datos.py`: Modelo de objetos con las clases `Actividad` y `Socio`, encapsulando métodos de negocio (`obtener_estado_cuota`, `necesita_aviso_cobro`, `esta_habilitado_para_ingreso`, `registrar_pago`).
- `logica.py`: Capa de persistencia en `clientes.json`, filtros de cobranza, estadísticas y reportes PDF con `fpdf2`.
- `main.py`: Ventana principal con barra de menús desplegables (`tk.Menu`), estilos `ttk` y tarjeta de resumen inicial.
- `pantalla_clientes.py`: Formulario con validaciones para registro de nuevos socios.
- `pantalla_edicion.py`: Formulario modal para modificar los datos de alumnos existentes con precarga automática.
- `pantalla_renovacion.py`: Módulo para buscar socio y registrar cobro de cuota con fecha real.
- `pantalla_estadisticas.py`: Panel visual de consultas con tabla `ttk.Treeview`, borrado múltiple y descarga de reportes.
- `pantalla_precios.py`: Ventana para modificar los aranceles de cuotas mensuales de cada actividad.
- `clientes.json`: Archivo local de persistencia con los datos de los alumnos e historial de pagos.
- `precios.json`: Archivo de configuración con los importes vigentes de las cuotas.

## 🚀 Requisitos y Ejecución

- **Python 3.10+** (o IDE Thonny)
- Librería `fpdf2`:
  ```bash
  pip install fpdf2