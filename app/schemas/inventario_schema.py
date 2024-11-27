from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InventarioBase(BaseModel):
    id_producto: int
    id_sucursal: int
    cantidad_disponible: int
    cantidad_maxima: int

class InventarioCreate(InventarioBase):
    pass

class InventarioUpdate(BaseModel):
    cantidad_disponible: Optional[int]
    cantidad_maxima: Optional[int]

class InventarioResponse(InventarioBase):
    id_inventario: int
    fecha_ultima_actualizacion: datetime

    class Config:
        from_attributes = True


class ProductoDetalle(BaseModel):
    nombre: str
    unidad_medida: str
    precio: float

class InventarioDetalleResponse(BaseModel):
    id_inventario: int
    id_producto: int
    id_sucursal: int
    cantidad_disponible: int
    cantidad_maxima: int
    fecha_ultima_actualizacion: datetime
    producto: ProductoDetalle
    costo_total: float

    class Config:
        from_attributes = True