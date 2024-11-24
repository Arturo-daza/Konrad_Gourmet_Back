from abc import ABC, abstractmethod

class ComponentePedido(ABC):
    @abstractmethod
    def calcular_total(self) -> float:
        """Calcula el total del componente (pedido o detalle)."""
        pass

    @abstractmethod
    def mostrar_detalles(self) -> dict:
        """Muestra los detalles del componente."""
        pass
