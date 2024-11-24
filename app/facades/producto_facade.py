from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app.models import Producto, CategoriaProducto, UnidadMedida
from app.schemas import ProductoCreate, ProductoBase


class ProductoFacade:
    def __init__(self, db: Session):
        self.db = db

    def crear_producto(self, producto_data: ProductoCreate):
        """Crea un nuevo producto."""
        # Validar que la categoría exista
        categoria = self.db.query(CategoriaProducto).filter_by(id_categoria=producto_data.id_categoria).first()
        if not categoria:
            raise ValueError(f"La categoría con ID {producto_data.id_categoria} no existe.")

        # Validar que la unidad de medida exista
        unidad = self.db.query(UnidadMedida).filter_by(id_unidad=producto_data.id_unidad_medida).first()
        if not unidad:
            raise ValueError(f"La unidad de medida con ID {producto_data.id_unidad_medida} no existe.")

        # Crear el producto
        producto = Producto(
            nombre=producto_data.nombre,
            id_categoria=producto_data.id_categoria,
            id_unidad_medida=producto_data.id_unidad_medida,
            precio=producto_data.precio,
        )
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)

        return producto

    def listar_productos(self):
        """Lista todos los productos."""
        return self.db.query(Producto).all()

    def obtener_producto(self, id_producto: int):
        """Obtiene un producto por su ID."""
        producto = self.db.query(Producto).filter_by(id_producto=id_producto).first()
        if not producto:
            raise NoResultFound(f"El producto con ID {id_producto} no existe.")
        return producto

    def actualizar_producto(self, id_producto: int, producto_data: ProductoBase):
        """Actualiza un producto."""
        producto = self.obtener_producto(id_producto)

        # Actualizar los campos
        producto.nombre = producto_data.nombre
        producto.id_categoria = producto_data.id_categoria
        producto.id_unidad_medida = producto_data.id_unidad_medida
        producto.precio = producto_data.precio

        self.db.commit()
        self.db.refresh(producto)
        return producto

    def eliminar_producto(self, id_producto: int):
        """Elimina un producto."""
        producto = self.obtener_producto(id_producto)
        self.db.delete(producto)
        self.db.commit()
        return {"message": f"Producto con ID {id_producto} eliminado exitosamente."}
