import uuid
from interfaces.servicio_base import ServicioBase

class MiServicio(ServicioBase):
    def __init__(self):
        self.id = uuid.uuid4()

    def procesar(self):
        print(f"[MiServicio] Procesando con ID: {self.id}")
