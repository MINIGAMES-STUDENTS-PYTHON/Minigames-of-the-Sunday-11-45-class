import injector
# from example import Servicio, ServicioConcreto, Cliente
from services.icliente import ICliente
from services.implementations.cliente import Cliente

# Módulo de inyección que configura las dependencias
class ModuloDeAplicacion(injector.Module):
    def configure(self, binder):
        # binder.bind(Servicio, to=ServicioConcreto)
        binder.bind(ICliente, to=Cliente)