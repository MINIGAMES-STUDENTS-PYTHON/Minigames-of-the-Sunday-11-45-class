import injector
from services.icliente import ICliente

class Cliente(ICliente):
    @injector.inject
    def __init__(self):
        pass
    def ejecutar_servicio(self) -> str:
        return "ejecutando servicio"