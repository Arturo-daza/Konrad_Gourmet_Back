from app.utils.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey, UniqueConstraint, String


# Tabla UnidadMedida
class UnidadMedida(Base):
    __tablename__ = "UnidadMedida"
    
    id_unidad = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), unique=True, nullable=False)
    
    # Relación con Producto y PlatoProducto
    productos = relationship("Producto", back_populates="unidad")
    plato_productos = relationship("PlatoProducto", back_populates="unidad")

class ConversionUnidades(Base):
    __tablename__ = "ConversionUnidades"

    id_unidad_base = Column(Integer, ForeignKey("UnidadMedida.id_unidad"), primary_key=True)
    id_unidad_convertida = Column(Integer, ForeignKey("UnidadMedida.id_unidad"), primary_key=True)
    factor_conversion = Column(Float, nullable=False)

    # Relaciones
    unidad_base = relationship("UnidadMedida", foreign_keys=[id_unidad_base])
    unidad_convertida = relationship("UnidadMedida", foreign_keys=[id_unidad_convertida])

    # Restricción de unicidad
    __table_args__ = (
        UniqueConstraint("id_unidad_base", "id_unidad_convertida", name="uq_conversion_unidades"),
    )

    def __repr__(self):
        return f"<ConversionUnidades(base={self.id_unidad_base}, convertida={self.id_unidad_convertida}, factor={self.factor_conversion})>"
