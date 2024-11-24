from sqlalchemy.orm import Session
from app.models import producto as Product, categoria_producto as Category


class ProductoManager:
    def __init__(self, db: Session):
        self.db = db

    def listar_categorias(self):
        """Lista todas las categorías de productos."""
        return self.db.query(Category).all()

    def listar_productos_por_categoria(self, id_categoria: int):
        """Lista productos por categoría."""
        return self.db.query(Product).filter(Product.id_categoria == id_categoria).all()
