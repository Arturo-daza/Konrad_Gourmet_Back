from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.inventario_schema import InventarioUpdate, InventarioResponse
from app.models.inventario import Inventario
from app.utils.database import DatabaseManager

router = APIRouter()

# Dependency
def get_db():
    db = DatabaseManager.get_instance().SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/{producto_id}", response_model=InventarioResponse)
def get_inventario(producto_id: int, db: Session = Depends(get_db)):
    inventario = db.query(Inventario).filter(Inventario.id_producto == producto_id).first()
    if not inventario:
        raise HTTPException(status_code=404, detail="Producto no encontrado en el inventario")
    return inventario


@router.put("/{producto_id}", response_model=InventarioResponse)
def update_inventario(producto_id: int, data: InventarioUpdate, db: Session = Depends(get_db)):
    inventario = db.query(Inventario).filter(Inventario.id_producto == producto_id).first()
    if not inventario:
        raise HTTPException(status_code=404, detail="Producto no encontrado en el inventario")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(inventario, key, value)
    db.commit()
    db.refresh(inventario)
    return inventario
