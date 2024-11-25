from app.utils.database import Base
from sqlalchemy import (
    Column, UniqueConstraint, Integer, ForeignKey, TIMESTAMP
)
from datetime import datetime
from sqlalchemy.orm import relationship
# Tabla Inventario
class Inventario(Base):
    __tablename__ = "Inventario"
    id_inventario = Column(Integer, primary_key=True, autoincrement=True)
    id_producto = Column(Integer, ForeignKey("Producto.id_producto"))
    id_sucursal = Column(Integer, ForeignKey("Sucursal.id_sucursal"))
    cantidad_disponible = Column(Integer, nullable=False)
    cantidad_maxima = Column(Integer, nullable=False)
    fecha_ultima_actualizacion = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)
   
    producto = relationship("Producto", back_populates="inventarios")
    sucursal = relationship("Sucursal", back_populates="inventarios")
    
    __table_args__ = (
        UniqueConstraint("id_producto", "id_sucursal", name="unique_producto_sucursal"),
    )