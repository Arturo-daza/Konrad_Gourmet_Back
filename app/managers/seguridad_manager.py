from datetime import datetime, timedelta
from fastapi import HTTPException
from jwt import encode, decode, exceptions
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.usuario import Usuario
from app.models.permiso import Permiso
from app.models.rol import Rol
from app.utils.database import DatabaseManager
import os

# Configuración para encriptación y JWT
# Cargar la clave secreta desde variables de entorno para mayor seguridad
SECRET_KEY = os.getenv("SECRET_KEY", "my_secrete_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 360
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SeguridadManager:
    def __init__(self, db: Session):
        self.db = db
    def autenticar_usuario(self, email: str, password: str) -> dict:
        """
        Autentica un usuario y devuelve un token si las credenciales son válidas.
        """
        try:
            user = self.db.query(Usuario).filter(Usuario.email == email).first()
            if not user or not pwd_context.verify(password, user.password):
                raise Exception("Credenciales inválidas")
            token = self._generar_token({"email": user.email, "rol": user.rol.nombre, "permisos": [p.nombre for p in user.rol.permisos]})
            return token
        except SQLAlchemyError as e:
            raise Exception(f"Error en la autenticación: {str(e)}")

    

    def crear_usuario(self, nombre: str, email: str, password: str, rol_id: int) -> Usuario:
        """
        Crea un nuevo usuario en la base de datos.
        """
        if self._correo_existe(email):
            raise ValueError("El correo ya está registrado.")
        
        if not self._validar_formato_password(password):
            raise ValueError("El formato de la contraseña no es válido.")
        
        
        hashed_password = self._encriptar_password(password)
        new_user = Usuario(nombre=nombre, email=email, password=hashed_password, id_rol=rol_id)
        
        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return new_user
        except SQLAlchemyError as e:
            raise Exception(f"Error creando usuario: {str(e)}")

    def validar_token(self, token: str) -> Usuario:
        """Valida el token JWT y devuelve el usuario autenticado."""
        try:
            data = decode(token, key=SECRET_KEY, algorithms=["HS256"])
            email = data.get("email")
            if not email:
                raise HTTPException(status_code=401, detail="Token inválido")
            
            usuario = self.db.query(Usuario).filter(Usuario.email == email).first()
            if not usuario:
                raise HTTPException(status_code=401, detail="Usuario no encontrado")
            return usuario
        except exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expirado")
        except exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Token inválido")

    def revocar_token(self, token: str):
        """
        Revoca un token (si fuera necesario implementar un mecanismo de lista negra).
        """
        # Aquí se puede implementar lógica para invalidar tokens si es necesario.
        pass

    # Métodos privados
    def _validar_formato_password(self, password: str) -> bool:
        """
        Valida que la contraseña cumpla con el formato requerido.
        """
        import re
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
        return bool(re.match(pattern, password))

    def _encriptar_password(self, password: str) -> str:
        """
        Encripta una contraseña usando bcrypt.
        """
        return pwd_context.hash(password)

    def _correo_existe(self, email: str) -> bool:
        """
        Verifica si un correo ya está registrado en la base de datos.
        """
        user = self.db.query(Usuario).filter(Usuario.email == email).first()
        return user is not None

    def _generar_token(self, data: dict) -> str:
        """
        Genera un token JWT.
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    def verificar_permisos(self, usuario: Usuario, permiso: str) -> bool:
        """Verifica si el usuario tiene el permiso especificado."""
        if not usuario.rol or not usuario.rol.permisos:
            return False
        permisos = [p.nombre for p in usuario.rol.permisos]  # Lista de nombres de permisos
        return permiso in permisos


    def obtener_usuario_actual(self):
        """Obtiene el usuario actualmente autenticado (simulado o basado en sesión)."""
        # Esto puede depender del contexto de la autenticación (por ejemplo, JWT o sesión)
        # En este caso, se valida directamente por el token
        raise NotImplementedError("Este método depende del flujo de autenticación")
