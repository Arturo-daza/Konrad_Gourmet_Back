from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.middlewares.jwt_bearer import JWTBearer
from app.utils.database import DatabaseManager
from app.facades.categoria_facade import CategoriaFacade
from app.schemas import CategoriaCreate, CategoriaResponse
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

@router.post("/", response_model=CategoriaResponse,  dependencies=[Depends(JWTBearer())])
def crear_categoria(
    categoria_data: CategoriaCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Crea una nueva categoría."""
    security_manager = SeguridadManager(db)
    usuario_actual = security_manager.validar_token(token)

    if not security_manager.verificar_permisos(usuario_actual, "Crear Categoría"):
        raise HTTPException(status_code=403, detail="No tienes permisos para crear categorías.")

    facade = CategoriaFacade(db)
    return facade.crear_categoria(categoria_data)

@router.get("/", response_model=list[CategoriaResponse],  dependencies=[Depends(JWTBearer())])
def listar_categorias(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Lista todas las categorías."""
    security_manager = SeguridadManager(db)
    usuario_actual = security_manager.validar_token(token)

    if not security_manager.verificar_permisos(usuario_actual, "Listar Categorías"):
        raise HTTPException(status_code=403, detail="No tienes permisos para listar categorías.")

    facade = CategoriaFacade(db)
    return facade.listar_categorias()

@router.get("/{id_categoria}", response_model=CategoriaResponse,  dependencies=[Depends(JWTBearer())])
def obtener_categoria(
    id_categoria: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Obtiene una categoría por su ID."""
    security_manager = SeguridadManager(db)
    usuario_actual = security_manager.validar_token(token)

    if not security_manager.verificar_permisos(usuario_actual, "Consultar Categoría"):
        raise HTTPException(status_code=403, detail="No tienes permisos para consultar categorías.")

    facade = CategoriaFacade(db)
    return facade.obtener_categoria(id_categoria)

@router.put("/{id_categoria}", response_model=CategoriaResponse,  dependencies=[Depends(JWTBearer())])
def actualizar_categoria(
    id_categoria: int,
    categoria_data: CategoriaCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Actualiza una categoría."""
    security_manager = SeguridadManager(db)
    usuario_actual = security_manager.validar_token(token)

    if not security_manager.verificar_permisos(usuario_actual, "Actualizar Categoría"):
        raise HTTPException(status_code=403, detail="No tienes permisos para actualizar categorías.")

    facade = CategoriaFacade(db)
    return facade.actualizar_categoria(id_categoria, categoria_data)

@router.delete("/{id_categoria}",  dependencies=[Depends(JWTBearer())])
def eliminar_categoria(
    id_categoria: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Elimina una categoría."""
    security_manager = SeguridadManager(db)
    usuario_actual = security_manager.validar_token(token)

    if not security_manager.verificar_permisos(usuario_actual, "Eliminar Categoría"):
        raise HTTPException(status_code=403, detail="No tienes permisos para eliminar categorías.")

    facade = CategoriaFacade(db)
    return facade.eliminar_categoria(id_categoria)
