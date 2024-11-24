from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from app.managers.seguridad_manager import SeguridadManager
from app.utils.database import DatabaseManager
from sqlalchemy.orm import Session

class JWTBearer(HTTPBearer):
    """
    Clase para la verificación de tokens JWT en las rutas protegidas.
    """
    async def __call__(self, request: Request):
        # Obtener las credenciales del encabezado Authorization
        auth = await super().__call__(request)
        
        # Obtener la sesión de base de datos
        db_instance = DatabaseManager.get_instance()
        db: Session = db_instance.SessionLocal()

        try:
            # Crear el SecurityManager con la sesión de base de datos
            seguridad_manager = SeguridadManager(db)

            # Validar el token y devolver el objeto Usuario
            usuario = seguridad_manager.validar_token(auth.credentials)

            # Verificar que el usuario exista
            if not usuario:
                raise HTTPException(status_code=403, detail="Usuario no encontrado o token inválido")

            return usuario  # Retornar el objeto Usuario
        finally:
            db.close()
