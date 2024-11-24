from app.utils.database import Base
from sqlalchemy import (
    Column, String, Integer, ForeignKey, Text, TIMESTAMP
)
from sqlalchemy.orm import relationship

# Tabla RegistroError
class RegistroError(Base):
    __tablename__ = "Registroerror"
    id_error = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("Usuario.id_usuario"))
    mensaje = Column(Text, nullable=False)
    fecha = Column(TIMESTAMP, nullable=False)
    modulo = Column(String(100), nullable=True)