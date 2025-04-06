class ServicioProvider:
    def __init__(self):
        self._servicios = {}

    def add_singleton(self, interface, implementacion):
        instancia = implementacion()
        self._servicios[interface] = lambda: instancia

    def add_transient(self, interface, implementacion):
        self._servicios[interface] = lambda: implementacion()

    def get(self, interface):
        creador = self._servicios.get(interface)
        if not creador:
            raise Exception(f"No se ha registrado el servicio para {interface}")
        return creador()
