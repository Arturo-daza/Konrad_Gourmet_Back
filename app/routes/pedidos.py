from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.pedido_schema import PedidoCreate, PedidoResponse
from app.models.pedido import Pedido
from app.utils.database import DatabaseManager

router = APIRouter()

# Dependency
def get_db():
    db = DatabaseManager.get_instance().SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=PedidoResponse)
def create_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    new_pedido = Pedido(**pedido.dict())
    db.add(new_pedido)
    db.commit()
    db.refresh(new_pedido)
    return new_pedido


@router.get("/{pedido_id}", response_model=PedidoResponse)
def get_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido
