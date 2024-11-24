from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.middlewares.jwt_bearer import JWTBearer
from app.utils.database import DatabaseManager
from app.facades.pedido_facade import PedidoFacade
from app.schemas import PedidoCreate, PedidoUpdate, PedidoResponse
from app.managers.seguridad_manager import SeguridadManager
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()

def get_db():
    db_instance = DatabaseManager.get_instance()
    db = db_instance.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PedidoResponse, dependencies=[Depends(JWTBearer())])
def registrar_pedido(
    pedido_data: PedidoCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Registra un nuevo pedido."""
    security_manager = SeguridadManager(db)
    usuario_actual = security_manager.validar_token(token)

    if not security_manager.verificar_permisos(usuario_actual, "Registrar Pedidos u Órdenes"):
        raise HTTPException(status_code=403, detail="No tienes permisos para registrar pedidos.")

    facade = PedidoFacade(db)
    return facade.crear_pedido(pedido_data)

@router.get("/", response_model=list[PedidoResponse], dependencies=[Depends(JWTBearer())])
def listar_pedidos(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Lista todos los pedidos."""
    security_manager = SeguridadManager(db)
    usuario_actual = security_manager.validar_token(token)

    if not security_manager.verificar_permisos(usuario_actual, "Listar Pedidos"):
        raise HTTPException(status_code=403, detail="No tienes permisos para listar pedidos.")

    facade = PedidoFacade(db)
    return facade.listar_pedidos()

@router.get("/{id_pedido}", response_model=PedidoResponse, dependencies=[Depends(JWTBearer())])
def obtener_pedido(
    id_pedido: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Obtiene un pedido por su ID."""
    security_manager = SeguridadManager(db)
    usuario_actual = security_manager.validar_token(token)

    if not security_manager.verificar_permisos(usuario_actual, "Consultar Pedido"):
        raise HTTPException(status_code=403, detail="No tienes permisos para consultar pedidos.")

    facade = PedidoFacade(db)
    return facade.obtener_pedido(id_pedido)

@router.put("/{id_pedido}", response_model=PedidoResponse, dependencies=[Depends(JWTBearer())])
def actualizar_pedido(
    id_pedido: int,
    pedido_data: PedidoUpdate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Actualiza un pedido."""
    security_manager = SeguridadManager(db)
    usuario_actual = security_manager.validar_token(token)

    if not security_manager.verificar_permisos(usuario_actual, "Actualizar Pedido"):
        raise HTTPException(status_code=403, detail="No tienes permisos para actualizar pedidos.")

    facade = PedidoFacade(db)
    return facade.actualizar_pedido(id_pedido, pedido_data)

@router.delete("/{id_pedido}", dependencies=[Depends(JWTBearer())])
def eliminar_pedido(
    id_pedido: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Elimina un pedido."""
    security_manager = SeguridadManager(db)
    usuario_actual = security_manager.validar_token(token)

    if not security_manager.verificar_permisos(usuario_actual, "Eliminar Pedido"):
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar pedidos.")

    facade = PedidoFacade(db)
    return facade.eliminar_pedido(id_pedido)
