# i_cliente.py
from abc import ABC, abstractmethod

class ICliente(ABC):
    @abstractmethod
    def ejecutar_servicio(self) -> str:
        pass


