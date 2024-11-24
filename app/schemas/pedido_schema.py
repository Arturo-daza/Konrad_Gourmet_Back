from typing import Optional, List
from pydantic import BaseModel, Field


class PedidoDetalleBase(BaseModel):
    id_plato: int
    cantidad: int
    precio_unitario: float
    observaciones: Optional[str]


class PedidoBase(BaseModel):
    mesa: int
    estado: str = Field(..., max_length=50)
    id_sucursal: int
    fecha: Optional[str] 


class PedidoCreate(PedidoBase):
    detalles: List[PedidoDetalleBase]


class PedidoResponse(PedidoBase):
    id_pedido: int
    detalles: List[PedidoDetalleBase]

    class Config:
        from_attributes = True
