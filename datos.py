class Socio:
    def __init__(self, dni, nombre, apellido, fecha_de_nacimiento, clase, apto_medico, estado="Activo", cuota_al_dia=False, mes_abonado="", dia_pago=0):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.nacimiento = fecha_de_nacimiento
        self.clase = clase
        self.apto_medico = apto_medico
        self.estado = estado
        self.cuota_al_dia = cuota_al_dia
        self.mes_abonado = mes_abonado
        self.dia_pago = dia_pago

    def to_dict(self):
        return {
            "dni": self.dni,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "fecha_de_nacimiento": self.nacimiento,
            "clase": self.clase,
            "apto_medico": self.apto_medico,
            "estado": self.estado,
            "cuota_al_dia": self.cuota_al_dia,
            "mes_abonado": self.mes_abonado,
            "dia_pago": self.dia_pago
        }