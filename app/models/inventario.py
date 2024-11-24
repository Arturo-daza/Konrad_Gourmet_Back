from app.utils.database import Base
from sqlalchemy import (
    Column, String, Integer, ForeignKey, TIMESTAMP
)
from sqlalchemy.orm import relationship
# Tabla Inventario
class Inventario(Base):
    __tablename__ = "Inventario"
    id_inventario = Column(Integer, primary_key=True, autoincrement=True)
    id_producto = Column(Integer, ForeignKey("Producto.id_producto"))
    id_sucursal = Column(Integer, ForeignKey("Sucursal.id_sucursal"))
    cantidad_disponible = Column(Integer, nullable=False)
    cantidad_maxima = Column(Integer, nullable=False)
    fecha_ultima_actualizacion = Column(TIMESTAMP, nullable=False)

    producto = relationship("Producto")
    sucursal = relationship("Sucursal")
