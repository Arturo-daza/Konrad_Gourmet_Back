from app.utils.database import Base
from sqlalchemy import (
    Column, String, Integer, ForeignKey, TIMESTAMP
)
from sqlalchemy.orm import relationship

# Tabla Pedido
class Pedido(Base):
    __tablename__ = "Pedido"
    id_pedido = Column(Integer, primary_key=True, autoincrement=True)
    mesa = Column(Integer, nullable=False)
    estado = Column(String(50), nullable=False)
    fecha = Column(TIMESTAMP, nullable=False)
    id_sucursal = Column(Integer, ForeignKey("Sucursal.id_sucursal"))

    sucursal = relationship("Sucursal", back_populates="pedidos")
    detalles = relationship("PedidoDetalle", back_populates="pedido")
