from app.utils.database import Base
from sqlalchemy import (
    Column, String, Integer
)
from sqlalchemy.orm import relationship
# Tabla Permiso
class Permiso(Base):
    __tablename__ = "Permiso"
    id_permiso = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), unique=True, nullable=False)

    roles = relationship("Rol", secondary="RolPermiso", back_populates="permisos")
