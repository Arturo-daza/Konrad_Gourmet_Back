from app.utils.database import Base
from sqlalchemy import (
    Column, String, Integer, ForeignKey, Text, TIMESTAMP
    )
from sqlalchemy.orm import relationship

# Tabla RegistroAuditoria
class RegistroAuditoria(Base):
    __tablename__ = "Registroauditoria"
    id_auditoria = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, ForeignKey("Usuario.id_usuario"))
    accion = Column(String(100), nullable=False)
    fecha = Column(TIMESTAMP, nullable=False)
    detalle = Column(Text, nullable=True)

