from app.utils.database import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

# Tabla CategoriaProducto
class CategoriaProducto(Base):
    __tablename__ = "CategoriaProducto"
    id_categoria = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), unique=True, nullable=False)
    
    productos = relationship("Producto", back_populates="categoria", cascade="all, delete-orphan")
