import injector
# from example import Servicio, ServicioConcreto, Cliente
from startup.service_collection_extensions import ModuloDeAplicacion
from services.icliente import ICliente

# Crear un injector y utilizarlo para obtener una instancia de Cliente
injector_obj = injector.Injector(ModuloDeAplicacion())
cliente = injector_obj.get(ICliente)


print(cliente.ejecutar_servicio())