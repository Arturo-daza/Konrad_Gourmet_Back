from app.utils.database import Base
from sqlalchemy import (
    Column, String, Integer
)
from sqlalchemy.orm import relationship


# Tabla Sucursal
class Sucursal(Base):
    __tablename__ = "Sucursal"
    id_sucursal = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(200), nullable=False)
    telefono = Column(String(15), nullable=False)

    # Relación con Inventario
    inventarios = relationship("Inventario", back_populates="sucursal")
    pedidos = relationship("Pedido", back_populates="sucursal")