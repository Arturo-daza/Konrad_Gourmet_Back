from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.database import DatabaseManager
from app.facades.plato_facade import PlatoFacade
from app.managers.seguridad_manager import SeguridadManager
from app.schemas import PlatoCreate, PlatoResponse
from fastapi.security import OAuth2PasswordBearer
from app.middlewares.jwt_bearer import JWTBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

router = APIRouter()

def get_db():
    db_instance = DatabaseManager.get_instance()
    db = db_instance.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PlatoResponse,  dependencies=[Depends(JWTBearer())])
def registrar_plato(
    plato_data: PlatoCreate,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    """Registra un nuevo plato o menú."""
    # Verificar permisos
    security_manager = SeguridadManager(db)
    
    usuario_actual = security_manager.validar_token(token)

    if not security_manager.verificar_permisos(usuario_actual, "Registrar Platos o Menús"):
        raise HTTPException(status_code=403, detail="No tienes permisos para registrar platos")

    # Registrar plato
    facade = PlatoFacade(db)
    return facade.registrar_plato(plato_data)
