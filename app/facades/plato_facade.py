from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app.models import Plato, PlatoProducto, Producto
from app.schemas import PlatoCreate, PlatoUpdate

class PlatoFacade:
    def __init__(self, db: Session):
        self.db = db

    def crear_plato(self, plato_data: PlatoCreate):
        """Crea un nuevo plato con ingredientes."""
        plato = Plato(
            nombre=plato_data.nombre,
            descripcion=plato_data.descripcion,
            precio=plato_data.precio
        )
        self.db.add(plato)
        self.db.commit()
        self.db.refresh(plato)

        for ingrediente in plato_data.ingredientes:
            producto = self.db.query(Producto).filter_by(id_producto=ingrediente.id_producto).first()
            if not producto:
                raise ValueError(f"El producto con ID {ingrediente.id_producto} no existe.")

            plato_ingrediente = PlatoProducto(
                id_plato=plato.id_plato,
                id_producto=ingrediente.id_producto,
                cantidad=ingrediente.cantidad,
                id_unidad_medida=ingrediente.id_unidad_medida
            )
            self.db.add(plato_ingrediente)

        self.db.commit()
        return plato

    def listar_platos(self):
        """Lista todos los platos."""
        return self.db.query(Plato).all()

    def obtener_plato(self, id_plato: int):
        """Obtiene un plato por su ID."""
        plato = self.db.query(Plato).filter_by(id_plato=id_plato).first()
        if not plato:
            raise NoResultFound(f"El plato con ID {id_plato} no existe.")
        return plato

    def actualizar_plato(self, id_plato: int, plato_data: PlatoUpdate):
        """Actualiza un plato y sus ingredientes."""
        plato = self.obtener_plato(id_plato)

        plato.nombre = plato_data.nombre
        plato.descripcion = plato_data.descripcion
        plato.precio = plato_data.precio

        # Actualizar ingredientes si se envían
        if plato_data.ingredientes:
            # Eliminar los ingredientes existentes
            self.db.query(PlatoProducto).filter_by(id_plato=id_plato).delete()

            # Agregar los nuevos ingredientes
            for ingrediente in plato_data.ingredientes:
                producto = self.db.query(Producto).filter_by(id_producto=ingrediente.id_producto).first()
                if not producto:
                    raise ValueError(f"El producto con ID {ingrediente.id_producto} no existe.")

                plato_ingrediente = PlatoProducto(
                    id_plato=id_plato,
                    id_producto=ingrediente.id_producto,
                    cantidad=ingrediente.cantidad,
                    id_unidad_medida=ingrediente.id_unidad_medida
                )
                self.db.add(plato_ingrediente)

        self.db.commit()
        self.db.refresh(plato)
        return plato

    def eliminar_plato(self, id_plato: int):
        """Elimina un plato."""
        plato = self.obtener_plato(id_plato)
        self.db.delete(plato)
        self.db.commit()
        return {"message": f"Plato con ID {id_plato} eliminado exitosamente."}
