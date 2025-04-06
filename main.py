from core.servicio_provider import ServicioProvider
from interfaces.servicio_base import ServicioBase
from services.mi_servicio import MiServicio
from app.controlador import Controlador

# Configuramos el contenedor de servicios
servicios = ServicioProvider()

# Puedes alternar entre Singleton y Transient
servicios.add_singleton(ServicioBase, MiServicio)
# servicios.add_transient(ServicioBase, MiServicio)

# Obtenemos servicios e inyectamos manualmente en el controlador
controlador1 = Controlador(servicios.get(ServicioBase))
controlador2 = Controlador(servicios.get(ServicioBase))

controlador1.ejecutar()
controlador2.ejecutar()

print("¿Misma instancia?", controlador1.servicio is controlador2.servicio)
