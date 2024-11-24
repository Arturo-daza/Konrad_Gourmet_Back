from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app.models import CategoriaProducto
from app.schemas import CategoriaCreate

class CategoriaFacade:
    def __init__(self, db: Session):
        self.db = db

    def crear_categoria(self, categoria_data: CategoriaCreate):
        """Crea una nueva categoría."""
        categoria = CategoriaProducto(nombre=categoria_data.nombre)
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def listar_categorias(self):
        """Lista todas las categorías."""
        return self.db.query(CategoriaProducto).all()

    def obtener_categoria(self, id_categoria: int):
        """Obtiene una categoría por su ID."""
        categoria = self.db.query(CategoriaProducto).filter_by(id_categoria=id_categoria).first()
        if not categoria:
            raise NoResultFound(f"La categoría con ID {id_categoria} no existe.")
        return categoria

    def actualizar_categoria(self, id_categoria: int, categoria_data: CategoriaCreate):
        """Actualiza una categoría."""
        categoria = self.obtener_categoria(id_categoria)
        categoria.nombre = categoria_data.nombre
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def eliminar_categoria(self, id_categoria: int):
        """Elimina una categoría."""
        categoria = self.obtener_categoria(id_categoria)
        self.db.delete(categoria)
        self.db.commit()
        return {"message": f"Categoría con ID {id_categoria} eliminada exitosamente."}
