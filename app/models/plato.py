from app.utils.database import Base
from sqlalchemy import (
    Column, String, Integer, ForeignKey, Text, DECIMAL
)
from sqlalchemy.orm import relationship

class Plato(Base):
    __tablename__ = "Plato"
    
    id_plato = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    precio = Column(DECIMAL(10, 2), nullable=False)
    
    # Relación con PlatoProducto
    ingredientes = relationship("PlatoProducto", back_populates="plato", cascade="all, delete")
    
class PlatoProducto(Base):
    __tablename__ = "PlatoProducto"
    
    id_plato = Column(Integer, ForeignKey("Plato.id_plato", ondelete="CASCADE"), primary_key=True)
    id_producto = Column(Integer, ForeignKey("Producto.id_producto", ondelete="CASCADE"), primary_key=True)
    cantidad = Column(DECIMAL(10, 2), nullable=False)
    id_unidad_medida = Column(Integer, ForeignKey("UnidadMedida.id_unidad", ondelete="CASCADE"), nullable=False)
    
    # Relaciones con Plato, Producto y UnidadMedida
    plato = relationship("Plato", back_populates="ingredientes")
    producto = relationship("Producto", back_populates="plato_productos")
    unidad = relationship("UnidadMedida", back_populates="plato_productos")
