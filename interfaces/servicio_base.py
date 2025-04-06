from abc import ABC, abstractmethod

class ServicioBase(ABC):
    @abstractmethod
    def procesar(self):
        pass
