from pydantic import BaseModel, Field
from typing import List, Optional

class ProductoBase(BaseModel):
    id_producto: int
    nombre: str
    id_categoria: int
    id_unidad_medida: int
    precio: float

class IngredienteCreate(BaseModel):
    id_producto: int
    cantidad: float
    id_unidad_medida: int

class PlatoBase(BaseModel):
    nombre: str = Field(..., max_length=100)
    descripcion: Optional[str]
    precio: float

class PlatoCreate(PlatoBase):
    ingredientes: List[IngredienteCreate]

class PlatoResponse(PlatoBase):
    id_plato: int
    ingredientes: List[IngredienteCreate]

    class Config:
        from_attributes = True
