from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional


class PermisoBase(BaseModel):
    id_permiso: int
    nombre: str

    class Config:
        from_attributes = True


class RolBase(BaseModel):
    id_rol: int
    nombre: str
    permisos: List[PermisoBase]

    class Config:
        from_attributes = True


class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr


class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=8)
    id_rol: int


class UsuarioResponse(UsuarioBase):
    id_usuario: int
    rol: RolBase

    class Config:
        from_attributes = True
