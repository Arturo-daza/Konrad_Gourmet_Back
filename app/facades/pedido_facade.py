
from sqlalchemy.orm import Session
from app.CompositePedido.pedido import Pedido
from app.CompositePedido.pedido_detalle import PedidoDetalle
from app.models import Plato, Pedido as PedidoORM, PedidoDetalle as PedidoDetalleORM
from app.schemas import PedidoCreate, PedidoUpdate


class PedidoFacade:
    def __init__(self, db: Session):
        self.db = db

    def crear_pedido(self, pedido_data: PedidoCreate):
        """Crea un nuevo pedido con detalles."""
        pedido = Pedido(
            mesa=pedido_data.mesa,
            estado="pendiente",
            fecha=pedido_data.fecha or "NOW()"
        )

        detalles_response = []  # Para almacenar los detalles que se devolverán

        for detalle_data in pedido_data.detalles:
            plato = self.db.query(Plato).filter_by(id_plato=detalle_data.id_plato).first()
            if not plato:
                raise ValueError(f"El plato con ID {detalle_data.id_plato} no existe.")

            detalle = PedidoDetalle(
                id_plato=detalle_data.id_plato,
                nombre=plato.nombre,
                cantidad=detalle_data.cantidad,
                precio_unitario=plato.precio,
            )
            pedido.agregar_detalle(detalle)

            # Añadir el detalle formateado para la respuesta
            detalles_response.append({
                "id_plato": detalle.id_plato,
                "cantidad": detalle.cantidad,
                "precio_unitario": detalle.precio_unitario,
                "subtotal": detalle.calcular_total(),
            })

        # Guardar en la base de datos
        pedido_orm = self._guardar_pedido_en_bd(pedido)

        # Devolver la respuesta
        return {
            "id_pedido": pedido_orm.id_pedido,
            "mesa": pedido.mesa,
            "estado": pedido.estado,
            "fecha": pedido.fecha,
            "total": pedido.calcular_total(),
            "detalles": detalles_response,
        }

    def listar_pedidos(self):
        """Lista todos los pedidos utilizando objetos Composite."""
        pedidos_orm = self.db.query(PedidoORM).all()
        pedidos = []

        for pedido_orm in pedidos_orm:
            pedido = self._convertir_a_composite(pedido_orm)

            # Formatear los detalles con los campos adicionales
            detalles_response = [
                {
                    "id_plato": detalle.id_plato,
                    "cantidad": detalle.cantidad,
                    "precio_unitario": detalle.precio_unitario,
                    "subtotal": detalle.calcular_total(),
                }
                for detalle in pedido.detalles
            ]

            pedidos.append({
                "id_pedido": pedido_orm.id_pedido,
                "mesa": pedido.mesa,
                "estado": pedido.estado,
                "fecha": pedido.fecha,
                "total": pedido.calcular_total(),
                "detalles": detalles_response,
            })

        return pedidos

    def obtener_pedido(self, id_pedido: int):
        """Obtiene un pedido por su ID utilizando objetos Composite."""
        pedido_orm = self.db.query(PedidoORM).filter_by(id_pedido=id_pedido).first()
        if not pedido_orm:
            raise ValueError(f"El pedido con ID {id_pedido} no existe.")

        pedido = self._convertir_a_composite(pedido_orm)

        # Formatear los detalles con los campos adicionales
        detalles_response = [
            {
                "id_plato": detalle.id_plato,
                "cantidad": detalle.cantidad,
                "precio_unitario": detalle.precio_unitario,
                "subtotal": detalle.calcular_total(),
            }
            for detalle in pedido.detalles
        ]

        return {
            "id_pedido": pedido_orm.id_pedido,
            "mesa": pedido.mesa,
            "estado": pedido.estado,
            "fecha": pedido.fecha,
            "total": pedido.calcular_total(),
            "detalles": detalles_response,
        }

    def actualizar_pedido(self, id_pedido: int, pedido_data: PedidoUpdate):
        """Actualiza un pedido completo, incluyendo su estado y detalles."""
        pedido_orm = self.db.query(PedidoORM).filter_by(id_pedido=id_pedido).first()
        if not pedido_orm:
            raise ValueError(f"El pedido con ID {id_pedido} no existe.")

        pedido_orm.mesa = pedido_data.mesa or pedido_orm.mesa
        pedido_orm.estado = pedido_data.estado or pedido_orm.estado
        self.db.commit()

        # Actualizar detalles si se proporcionan
        if pedido_data.detalles:
            self.db.query(PedidoDetalleORM).filter_by(id_pedido=id_pedido).delete()

            for detalle_data in pedido_data.detalles:
                plato = self.db.query(Plato).filter_by(id_plato=detalle_data.id_plato).first()
                if not plato:
                    raise ValueError(f"El plato con ID {detalle_data.id_plato} no existe.")

                nuevo_detalle = PedidoDetalleORM(
                    id_pedido=id_pedido,
                    id_plato=detalle_data.id_plato,
                    cantidad=detalle_data.cantidad,
                    precio_unitario=plato.precio
                )
                self.db.add(nuevo_detalle)
            self.db.commit()

        return self.obtener_pedido(id_pedido)

    def eliminar_pedido(self, id_pedido: int):
        """Elimina un pedido por su ID."""
        pedido_orm = self.db.query(PedidoORM).filter_by(id_pedido=id_pedido).first()
        if not pedido_orm:
            raise ValueError(f"El pedido con ID {id_pedido} no existe.")

        self.db.query(PedidoDetalleORM).filter_by(id_pedido=id_pedido).delete()
        self.db.delete(pedido_orm)
        self.db.commit()
        return {"message": f"Pedido con ID {id_pedido} eliminado exitosamente."}

    def _guardar_pedido_en_bd(self, pedido: Pedido):
        """Guarda un pedido y sus detalles en la base de datos."""
        nuevo_pedido = PedidoORM(
            mesa=pedido.mesa,
            estado=pedido.estado,
            fecha=pedido.fecha
        )
        self.db.add(nuevo_pedido)
        self.db.commit()
        self.db.refresh(nuevo_pedido)

        for detalle in pedido.detalles:
            nuevo_detalle = PedidoDetalleORM(
                id_pedido=nuevo_pedido.id_pedido,
                id_plato=detalle.id_plato,
                cantidad=detalle.cantidad,
                precio_unitario=detalle.precio_unitario,
            )
            self.db.add(nuevo_detalle)
        self.db.commit()

        return nuevo_pedido

    def _convertir_a_composite(self, pedido_orm: PedidoORM):
        """Convierte un objeto ORM en un Composite."""
        pedido = Pedido(
            mesa=pedido_orm.mesa,
            estado=pedido_orm.estado,
            fecha=pedido_orm.fecha
        )
        pedido.id_pedido = pedido_orm.id_pedido  # Asegura que el ID esté presente

        detalles_orm = self.db.query(PedidoDetalleORM).filter_by(id_pedido=pedido_orm.id_pedido).all()

        for detalle_orm in detalles_orm:
            detalle = PedidoDetalle(
                id_plato=detalle_orm.id_plato,
                nombre=detalle_orm.plato.nombre,
                cantidad=detalle_orm.cantidad,
                precio_unitario=detalle_orm.precio_unitario,
            )
            pedido.agregar_detalle(detalle)

        # Calcula el total del pedido
        pedido.total = pedido.calcular_total()
        return pedido


