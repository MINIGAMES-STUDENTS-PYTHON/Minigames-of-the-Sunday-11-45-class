from interfaces.servicio_base import ServicioBase

class Controlador:
    def __init__(self, servicio: ServicioBase):
        self.servicio = servicio

    def ejecutar(self):
        self.servicio.procesar()
