from sqlalchemy.orm import Session
from app.models import Plato, PlatoProducto, Producto
from app.schemas import PlatoCreate

class PlatoFacade:
    def __init__(self, db: Session):
        self.db = db

    def registrar_plato(self, plato_data: PlatoCreate):
        """Registra un nuevo plato y sus ingredientes."""
        # Crear el plato
        plato = Plato(
            nombre=plato_data.nombre,
            descripcion=plato_data.descripcion,
            precio=plato_data.precio,
        )
        self.db.add(plato)
        self.db.commit()
        self.db.refresh(plato)

        # Agregar los ingredientes
        for ingrediente in plato_data.ingredientes:
            # Verificar que el producto exista
            producto = self.db.query(Producto).filter_by(id_producto=ingrediente.id_producto).first()
            if not producto:
                raise ValueError(f"El producto con ID {ingrediente.id_producto} no existe.")

            # Crear la relación PlatoProducto
            plato_producto = PlatoProducto(
                id_plato=plato.id_plato,
                id_producto=ingrediente.id_producto,
                cantidad=ingrediente.cantidad,
                id_unidad_medida=ingrediente.id_unidad_medida,
            )
            self.db.add(plato_producto)

        self.db.commit()
        return plato
