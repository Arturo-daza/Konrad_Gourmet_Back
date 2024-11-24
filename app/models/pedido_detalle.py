from app.utils.database import Base
from sqlalchemy import (
    Column, Integer, ForeignKey, Text, DECIMAL
)
from sqlalchemy.orm import relationship

# Tabla PedidoDetalle
class PedidoDetalle(Base):
    __tablename__ = "PedidoDetalle"
    id_pedido = Column(Integer, ForeignKey("Pedido.id_pedido"), primary_key=True)
    id_plato = Column(Integer, ForeignKey("Plato.id_plato"), primary_key=True)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(DECIMAL(10, 2), nullable=True)
    observaciones = Column(Text, nullable=True)

    pedido = relationship("Pedido", back_populates="detalles")
    plato = relationship("Plato")
