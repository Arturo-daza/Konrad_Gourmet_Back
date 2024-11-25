from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PedidoDetalleBase(BaseModel):
    id_plato: int
    cantidad: int
    
    
class PedidoDetalleResponse(PedidoDetalleBase):
    precio_unitario: float
    subtotal: float

class PedidoBase(BaseModel):
    mesa: int
    fecha: Optional[datetime] = datetime.now()
    id_sucursal: Optional[int] = 1

class PedidoCreate(PedidoBase):
    detalles: List[PedidoDetalleBase]

class PedidoUpdate(PedidoBase):
    estado: Optional[str]
    detalles: Optional[List[PedidoDetalleBase]]
    class Config:
        extra = "ignore"

class PedidoResponse(PedidoBase):
    id_pedido: int
    estado: str
    total: float
    detalles: List[PedidoDetalleResponse]

    class Config:
        from_attributes = True
