from typing import List
from .pedido_detalle import PedidoDetalle  # Importa los detalles del pedido
from .componente_pedido import ComponentePedido  # Importa la clase abstracta

class Pedido(ComponentePedido):
    def __init__(self, mesa: int, estado: str, fecha: str):
        self.mesa = mesa
        self.estado = estado
        self.fecha = fecha
        self.detalles: List[PedidoDetalle] = []  # Lista de detalles del pedido

    def agregar_detalle(self, detalle: PedidoDetalle):
        """Agrega un detalle al pedido."""
        self.detalles.append(detalle)

    def calcular_total(self) -> float:
        """Suma el total de todos los detalles."""
        return sum(detalle.calcular_total() for detalle in self.detalles)

    def mostrar_detalles(self) -> dict:
        """Muestra el pedido y sus detalles."""
        return {
            "mesa": self.mesa,
            "estado": self.estado,
            "fecha": self.fecha,
            "total": self.calcular_total(),
            "detalles": [detalle.mostrar_detalles() for detalle in self.detalles],
        }
