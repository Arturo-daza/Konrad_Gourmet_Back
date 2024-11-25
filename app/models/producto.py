from app.utils.database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship

# Tabla Producto
class Producto(Base):
    __tablename__ = "Producto"
    
    id_producto = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    id_categoria = Column(Integer, ForeignKey("CategoriaProducto.id_categoria"))
    id_unidad_medida = Column(Integer, ForeignKey("UnidadMedida.id_unidad"))
    precio = Column(DECIMAL(10, 2), nullable=False)
    
    # Relaciones con CategoriaProducto, UnidadMedida y PlatoProducto
    categoria = relationship("CategoriaProducto", back_populates="productos")
    unidad = relationship("UnidadMedida", back_populates="productos")
    plato_productos = relationship("PlatoProducto", back_populates="producto")
    
    # Relación con Inventario
    inventarios = relationship("Inventario", back_populates="producto")
