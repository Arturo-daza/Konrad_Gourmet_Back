from app.utils.database import Base
from sqlalchemy import (
    Column, String, Integer
)

# Tabla Sucursal
class Sucursal(Base):
    __tablename__ = "Sucursal"
    id_sucursal = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(200), nullable=False)
    telefono = Column(String(15), nullable=False)
