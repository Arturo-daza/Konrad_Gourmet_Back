from pydantic import BaseModel, Field

class CategoriaBase(BaseModel):
    nombre: str = Field(..., max_length=50)

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaResponse(CategoriaBase):
    id_categoria: int

    class Config:
        from_attributes = True
