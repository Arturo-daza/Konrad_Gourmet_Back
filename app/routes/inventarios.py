from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.middlewares.jwt_bearer import JWTBearer
from app.utils.database import DatabaseManager
from app.facades.inventario_facade import InventarioFacade
from app.schemas import InventarioCreate, InventarioUpdate, InventarioResponse
from fastapi.security import OAuth2PasswordBearer
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

@router.post("/", response_model=InventarioResponse, dependencies=[Depends(JWTBearer())])
@router.post("/", response_model=InventarioResponse)
def crear_inventario(
    inventario_data: InventarioCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    seguridad_manager = SeguridadManager(db)
    usuario_actual = seguridad_manager.validar_token(token)

    if not seguridad_manager.verificar_permisos(usuario_actual, "Crear Inventario"):
        raise HTTPException(status_code=403, detail="No tienes permisos para crear inventario.")

    facade = InventarioFacade(db)
    return facade.crear_inventario(
        inventario_data.id_producto,
        inventario_data.id_sucursal,
        inventario_data.cantidad_disponible,
        inventario_data.cantidad_maxima,
    )

@router.put("/{id_inventario}", response_model=InventarioResponse, dependencies=[Depends(JWTBearer())])
def actualizar_inventario(
    id_inventario: int,
    inventario_data: InventarioUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Actualiza un registro de inventario."""
    seguridad_manager = SeguridadManager(db)
    usuario_actual = seguridad_manager.validar_token(token)

    if not seguridad_manager.verificar_permisos(usuario_actual, "Actualizar Inventario"):
        raise HTTPException(status_code=403, detail="No tienes permisos para actualizar inventario.")

    facade = InventarioFacade(db)
    return facade.actualizar_inventario(
        id_inventario,
        inventario_data.cantidad_disponible,
        inventario_data.cantidad_maxima,
    )

@router.get("/{id_sucursal}", response_model=list[InventarioResponse], dependencies=[Depends(JWTBearer())])
def obtener_inventario_por_sucursal(
    id_sucursal: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Obtiene el inventario de una sucursal."""
    seguridad_manager = SeguridadManager(db)
    usuario_actual = seguridad_manager.validar_token(token)

    if not seguridad_manager.verificar_permisos(usuario_actual, "Consultar Inventario"):
        raise HTTPException(status_code=403, detail="No tienes permisos para consultar inventario.")

    facade = InventarioFacade(db)
    return facade.obtener_inventario_por_sucursal(id_sucursal)

@router.delete("/{id_inventario}", dependencies=[Depends(JWTBearer())])
def eliminar_inventario(
    id_inventario: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Elimina un registro de inventario."""
    seguridad_manager = SeguridadManager(db)
    usuario_actual = seguridad_manager.validar_token(token)

    if not seguridad_manager.verificar_permisos(usuario_actual, "Eliminar Inventario"):
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar inventario.")

    facade = InventarioFacade(db)
    facade.eliminar_inventario(id_inventario)
    return {"message": f"Inventario con ID {id_inventario} eliminado exitosamente."}


