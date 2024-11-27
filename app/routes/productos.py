from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.schemas.producto_schema import ProductoIDs
from app.utils.database import DatabaseManager
from app.facades.producto_facade import ProductoFacade
from app.schemas import ProductoCreate, ProductoBase, ProductoResponse
from app.middlewares.jwt_bearer import JWTBearer
from app.managers.seguridad_manager import SeguridadManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()

def get_db():
    db_instance = DatabaseManager.get_instance()
    db = db_instance.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ProductoResponse,  dependencies=[Depends(JWTBearer())])
def crear_producto(
    producto_data: ProductoCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Crea un nuevo producto."""
    security_manager = SeguridadManager(db)
    usuario_actual = security_manager.validar_token(token)
    print(usuario_actual)

    if not security_manager.verificar_permisos(usuario_actual, "Crear Producto"):
        raise HTTPException(status_code=403, detail="No tienes permisos para crear productos.")

    facade = ProductoFacade(db)
    return facade.crear_producto(producto_data)

@router.get("/", response_model=list[ProductoResponse],  dependencies=[Depends(JWTBearer())])
def listar_productos(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Lista todos los productos."""
    security_manager = SeguridadManager(db)
    usuario_actual = security_manager.validar_token(token)

    if not security_manager.verificar_permisos(usuario_actual, "Listar Productos"):
        raise HTTPException(status_code=403, detail="No tienes permisos para listar productos.")

    facade = ProductoFacade(db)
    return facade.listar_productos()

@router.get("/{id_producto}", response_model=ProductoResponse,  dependencies=[Depends(JWTBearer())])
def obtener_producto(
    id_producto: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Obtiene un producto por su ID."""
    security_manager = SeguridadManager(db)
    usuario_actual = security_manager.validar_token(token)

    if not security_manager.verificar_permisos(usuario_actual, "Consultar Producto"):
        raise HTTPException(status_code=403, detail="No tienes permisos para consultar productos.")

    facade = ProductoFacade(db)
    return facade.obtener_producto(id_producto)

@router.put("/{id_producto}", response_model=ProductoBase,  dependencies=[Depends(JWTBearer())])
def actualizar_producto(
    id_producto: int,
    producto_data: ProductoBase,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Actualiza un producto."""
    security_manager = SeguridadManager(db)
    usuario_actual = security_manager.validar_token(token)

    if not security_manager.verificar_permisos(usuario_actual, "Actualizar Producto"):
        raise HTTPException(status_code=403, detail="No tienes permisos para actualizar productos.")

    facade = ProductoFacade(db)
    return facade.actualizar_producto(id_producto, producto_data)

@router.delete("/{id_producto}", dependencies=[Depends(JWTBearer())])
def eliminar_producto(
    id_producto: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Elimina un producto."""
    security_manager = SeguridadManager(db)
    usuario_actual = security_manager.validar_token(token)

    if not security_manager.verificar_permisos(usuario_actual, "Eliminar Producto"):
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar productos.")

    facade = ProductoFacade(db)
    return facade.eliminar_producto(id_producto)

@router.post("/batch", response_model=List[ProductoResponse], dependencies=[Depends(JWTBearer())])
def obtener_productos_batch(
    producto_ids: ProductoIDs,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Obtiene múltiples productos pasando una lista de IDs."""
    security_manager = SeguridadManager(db)
    usuario_actual = security_manager.validar_token(token)

    if not security_manager.verificar_permisos(usuario_actual, "Listar Productos"):
        raise HTTPException(status_code=403, detail="No tienes permisos para listar productos.")

    facade = ProductoFacade(db)
    return facade.obtener_productos_batch(producto_ids.ids_producto)
