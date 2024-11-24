from app.utils.database import Base
from sqlalchemy import (
    Column, String, Integer, ForeignKey
)
from sqlalchemy.orm import relationship

# Tabla Usuario
class Usuario(Base):
    __tablename__ = "Usuario"
    id_usuario = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    id_rol = Column(Integer, ForeignKey("Rol.id_rol"))

    rol = relationship("Rol", back_populates="usuarios")