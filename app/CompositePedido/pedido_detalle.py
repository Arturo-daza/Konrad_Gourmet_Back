from .componente_pedido import ComponentePedido
class PedidoDetalle(ComponentePedido):
    def __init__(self, id_plato: int, nombre: str, cantidad: int, precio_unitario: float):
        self.id_plato = id_plato
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario

    def calcular_total(self) -> float:
        """Calcula el subtotal del detalle."""
        return self.cantidad * self.precio_unitario

    def mostrar_detalles(self) -> dict:
        """Muestra los detalles del ítem."""
        return {
            "id_plato": self.id_plato,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio_unitario": self.precio_unitario,
            "subtotal": self.calcular_total(),
        }
