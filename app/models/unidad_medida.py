from app.utils.database import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

# Tabla UnidadMedida
class UnidadMedida(Base):
    __tablename__ = "UnidadMedida"
    
    id_unidad = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), unique=True, nullable=False)
    
    # Relación con Producto y PlatoProducto
    productos = relationship("Producto", back_populates="unidad")
    plato_productos = relationship("PlatoProducto", back_populates="unidad")
