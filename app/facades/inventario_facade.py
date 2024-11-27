from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional
from app.models.inventario import Inventario
from app.models.plato import PlatoProducto
from app.models.producto import Producto
from datetime import datetime
from app.models import ConversionUnidades


class InventarioFacade:
    def __init__(self, db: Session):
        self.db = db

    def crear_inventario(self, id_producto: int, id_sucursal: int, cantidad_disponible: int, cantidad_maxima: int):
        """Crea un registro de inventario."""
        try:
            inventario = Inventario(
                id_producto=id_producto,
                id_sucursal=id_sucursal,
                cantidad_disponible=cantidad_disponible,
                cantidad_maxima=cantidad_maxima,
                fecha_ultima_actualizacion=datetime.utcnow()
            )
            self.db.add(inventario)
            self.db.commit()
            return inventario
        except SQLAlchemyError as e:
            self.db.rollback()
            raise ValueError(f"Error al crear inventario: {str(e)}")

    def actualizar_inventario(self, id_inventario: int, cantidad_disponible: Optional[int] = None, cantidad_maxima: Optional[int] = None):
        """Actualiza un registro de inventario."""
        inventario = self.db.query(Inventario).filter_by(id_inventario=id_inventario).first()
        if not inventario:
            raise ValueError("El registro de inventario no existe.")

        if cantidad_disponible is not None:
            inventario.cantidad_disponible = cantidad_disponible
        if cantidad_maxima is not None:
            inventario.cantidad_maxima = cantidad_maxima

        inventario.fecha_ultima_actualizacion = datetime.utcnow()
        self.db.commit()
        return inventario

    def obtener_inventario_por_sucursal(self, id_sucursal: int):
        """Obtiene todos los productos de una sucursal."""
        return self.db.query(Inventario).filter_by(id_sucursal=id_sucursal).all()

    def obtener_inventario_por_producto(self, id_producto: int):
        """Obtiene el inventario de un producto específico."""
        return self.db.query(Inventario).filter_by(id_producto=id_producto).all()

    def eliminar_inventario(self, id_inventario: int):
        """Elimina un registro de inventario."""
        inventario = self.db.query(Inventario).filter_by(id_inventario=id_inventario).first()
        if not inventario:
            raise ValueError("El registro de inventario no existe.")

        self.db.delete(inventario)
        self.db.commit()


    def verificar_stock_bajo(self, id_sucursal: int):
        """Verifica el stock bajo de una sucursal."""
        productos_bajo_stock = self.db.query(Inventario).filter(
            Inventario.id_sucursal == id_sucursal,
            Inventario.cantidad_disponible <= (Inventario.cantidad_maxima * 0.25)
        ).all()

        return [
            {
                "id_producto": p.id_producto,
                "cantidad_disponible": p.cantidad_disponible,
                "cantidad_maxima": p.cantidad_maxima
            }
            for p in productos_bajo_stock
        ]
        
    def convertir_unidades(self, cantidad, id_unidad_origen: int, id_unidad_destino: int) -> float:
        if id_unidad_origen == id_unidad_destino:
            return float(cantidad)

        conversion = self.db.query(ConversionUnidades).filter_by(
            id_unidad_base=id_unidad_origen,
            id_unidad_convertida=id_unidad_destino
        ).first()

        if not conversion:
            raise ValueError(f"No existe factor de conversión entre las unidades {id_unidad_origen} y {id_unidad_destino}")

        return float(cantidad) * float(conversion.factor_conversion)



    
    def ajustar_inventario_por_pedido(self, id_sucursal: int, detalles_pedido: List[dict]):

        for detalle in detalles_pedido:
            ingredientes = self.db.query(PlatoProducto).filter_by(id_plato=detalle["id_plato"]).all()

            if not ingredientes:
                raise ValueError(f"El plato con ID {detalle['id_plato']} no tiene ingredientes asociados.")
            for ingrediente in ingredientes:
                producto = self.db.query(Producto).filter_by(id_producto=ingrediente.id_producto).first()

                if not producto:
                    raise ValueError(f"El producto con ID {ingrediente.id_producto} no existe.")
                
                inventario = self.db.query(Inventario).filter_by(
                    id_producto=ingrediente.id_producto,
                    id_sucursal=id_sucursal
                ).first()

                if not inventario:
                    raise ValueError(f"No hay inventario para el producto con ID {ingrediente.id_producto} en la sucursal {id_sucursal}")

                cantidad_requerida = float(detalle["cantidad"]) * float(ingrediente.cantidad)



                cantidad_convertida = self.convertir_unidades(
                    cantidad=cantidad_requerida,
                    id_unidad_origen=ingrediente.id_unidad_medida,
                    id_unidad_destino=producto.id_unidad_medida
                )
                
                if inventario.cantidad_disponible < cantidad_convertida:
                    raise ValueError(f"No hay suficiente inventario para el producto {producto.nombre}. Disponible: {inventario.cantidad_disponible}, Requerido: {cantidad_convertida}")

                # Descontar del inventario
                inventario.cantidad_disponible -= cantidad_convertida

        # Mover el commit fuera de los bucles
        self.db.commit()
        
    

    def obtener_inventario_con_detalles(self, id_sucursal: int):
        """
        Obtiene el inventario de una sucursal con los detalles del producto y el costo total calculado.
        """
        inventario = (
            self.db.query(Inventario)
            .options(joinedload(Inventario.producto))  # Cargar detalles de producto
            .filter(Inventario.id_sucursal == id_sucursal)
            .all()
        )

        resultado = []
        for item in inventario:
            producto = item.producto
            costo_total = item.cantidad_disponible * producto.precio
            resultado.append({
                "id_inventario": item.id_inventario,
                "id_producto": item.id_producto,
                "id_sucursal": item.id_sucursal,
                "cantidad_disponible": item.cantidad_disponible,
                "cantidad_maxima": item.cantidad_maxima,
                "fecha_ultima_actualizacion": item.fecha_ultima_actualizacion,
                "producto": {
                    "nombre": producto.nombre,
                    "unidad_medida": producto.unidad.nombre,
                    "precio": producto.precio
                },
                "costo_total": costo_total
            })
            
        return resultado
    
    def obtener_inventario_por_id(self, id_inventario: int):
        """
        Obtiene un inventario específico con detalles del producto.
        """
        inventario = (
            self.db.query(Inventario)
            .options(joinedload(Inventario.producto))  # Cargar detalles de producto
            .filter(Inventario.id_inventario == id_inventario)
            .first()
        )

        if not inventario:
            raise ValueError(f"Inventario con ID {id_inventario} no encontrado.")

        producto = inventario.producto
        costo_total = inventario.cantidad_disponible * producto.precio
        return {
            "id_inventario": inventario.id_inventario,
            "id_producto": inventario.id_producto,
            "id_sucursal": inventario.id_sucursal,
            "cantidad_disponible": inventario.cantidad_disponible,
            "cantidad_maxima": inventario.cantidad_maxima,
            "fecha_ultima_actualizacion": inventario.fecha_ultima_actualizacion,
            "producto": {
                "nombre": producto.nombre,
                "unidad_medida": producto.unidad.nombre,
                "precio": producto.precio
            },
            "costo_total": costo_total
        }
        
    def recepcionar_unidades(self, id_inventario: int, cantidad: int):
        """
        Incrementa la cantidad disponible en el inventario.
        """
        inventario = self.db.query(Inventario).filter(Inventario.id_inventario == id_inventario).first()
        if not inventario:
            raise ValueError(f"Inventario con ID {id_inventario} no encontrado.")

        inventario.cantidad_disponible += cantidad
        inventario.fecha_ultima_actualizacion = datetime.utcnow()
        self.db.commit()
        # Retornar el inventario actualizado con los datos completos
        return {
            "id_inventario": inventario.id_inventario,
            "id_producto": inventario.id_producto,
            "id_sucursal": inventario.id_sucursal,
            "cantidad_disponible": inventario.cantidad_disponible,
            "cantidad_maxima": inventario.cantidad_maxima,
            "fecha_ultima_actualizacion": inventario.fecha_ultima_actualizacion,
        }



                
