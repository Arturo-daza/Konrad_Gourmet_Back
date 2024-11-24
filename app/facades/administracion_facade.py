from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.permiso import Permiso

from app.schemas.user_schema import UsuarioCreate, UsuarioResponse, RolBase
from app.managers.seguridad_manager import SeguridadManager


class AdministrationFacade:
    def __init__(self, db: Session):
        self.db = db
        self.security_manager = SeguridadManager(db)

    def crear_usuario(self, user_data: UsuarioCreate) -> UsuarioResponse:
        """Crea un usuario y devuelve un esquema Pydantic serializable."""
        user = self.security_manager.crear_usuario(
            nombre=user_data.nombre,
            email=user_data.email,
            password=user_data.password,
            rol_id=user_data.id_rol
        )
        return UsuarioResponse.from_orm(user)

    def get_users(self) -> list[UsuarioResponse]:
        """Obtiene todos los usuarios del sistema."""
        users = self.security_manager.get_all_users()
        return [UsuarioResponse.from_orm(user) for user in users]

    def create_role(self, role_data: RolBase) -> dict:
        """Crea un nuevo rol en el sistema."""
        role = Rol(nombre=role_data.nombre)
        self.db.add(role)
        self.db.commit()
        return {"message": f"Rol '{role.nombre}' creado exitosamente."}

    def assign_permissions_to_role(self, role_id: int, permissions: list[int]) -> dict:
        """Asigna permisos a un rol existente."""
        role = self.db.query(Rol).get(role_id)
        if not role:
            raise ValueError(f"Rol con ID {role_id} no encontrado.")
        for perm_id in permissions:
            permission = self.db.query(Permiso).get(perm_id)
            if permission:
                role.permisos.append(permission)
        self.db.commit()
        return {"message": f"Permisos asignados al rol '{role.nombre}'."}

