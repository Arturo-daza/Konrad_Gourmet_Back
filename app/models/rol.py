from app.utils.database import Base
from sqlalchemy import (
    Column, String, Integer, ForeignKey
)
from sqlalchemy.orm import relationship

# Tabla Rol
class Rol(Base):
    __tablename__ = "Rol"
    id_rol = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), unique=True, nullable=False)

    permisos = relationship("Permiso", secondary="RolPermiso", back_populates="roles")
    usuarios = relationship("Usuario", back_populates="rol")

# Tabla RolPermiso
class RolPermiso(Base):
    __tablename__ = "RolPermiso"
    id_rol = Column(Integer, ForeignKey("Rol.id_rol"), primary_key=True)
    id_permiso = Column(Integer, ForeignKey("Permiso.id_permiso"), primary_key=True)