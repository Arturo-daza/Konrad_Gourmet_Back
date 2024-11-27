from typing import List
from pydantic import BaseModel, Field

class ProductoBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    id_categoria: int
    id_unidad_medida: int
    precio: float

class ProductoCreate(ProductoBase):
    pass

class ProductoResponse(ProductoBase):
    id_producto: int

    class Config:
        from_attributes = True
        
# Nuevo modelo Pydantic para recibir una lista de IDs
class ProductoIDs(BaseModel):
    ids_producto: List[int]
