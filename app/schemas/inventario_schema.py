from pydantic import BaseModel
from typing import Optional


class InventarioBase(BaseModel):
    id_producto: int
    id_sucursal: int
    cantidad_disponible: int
    cantidad_maxima: int


class InventarioUpdate(BaseModel):
    cantidad_disponible: Optional[int]
    cantidad_maxima: Optional[int]


class InventarioResponse(InventarioBase):
    id_inventario: int

    class Config:
        from_attributes = True
