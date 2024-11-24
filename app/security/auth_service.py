import os
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from app.models.usuario import Usuario
from app.models.rol import Rol
from app.models.permiso import Permiso
from fastapi import HTTPException
from jwt import encode, decode, exceptions

SECRET_KEY = os.getenv("SECRET_KEY", "my_secret_key")


class SecurityManager:
    def __init__(self, db: Session):
        self.db = db

    def autenticarUsuario(self, email: str, password: str) -> str:
        """Autentica un usuario y genera un token si las credenciales son correctas."""
        user = self.db.query(Usuario).filter(Usuario.email == email).first()
        if not user or not bcrypt.verify(password, user.password):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
        token = self._crearToken({"user_id": user.id, "email": user.email})
        return token

    def verificarPermisos(self, usuario: Usuario, permiso: str) -> bool:
        """Verifica si un usuario tiene un permiso específico."""
        role = self.db.query(Rol).filter(Rol.id == usuario.id_rol).first()
        if not role:
            return False
        permisos = [p.nombre for p in role.permisos]
        return permiso in permisos

    def create_user(self, nombre: str, email: str, password: str, rolId: int) -> Usuario:
        """Crea un nuevo usuario con rol asignado."""
        if self._correoExiste(email):
            raise HTTPException(status_code=400, detail="El correo ya está registrado")
        if not self._validarFormatoPassword(password):
            raise HTTPException(status_code=400, detail="La contraseña no cumple los requisitos")
        hashed_password = self._encriptarPassword(password)
        user = Usuario(nombre=nombre, email=email, password=hashed_password, id_rol=rolId)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def updateUsuario(self, user_id: int, user_data: dict) -> Usuario:
        """Actualiza un usuario existente."""
        user = self.db.query(Usuario).get(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        for key, value in user_data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def validarToken(self, token: str) -> Usuario:
        """Valida un token JWT y devuelve el usuario correspondiente."""
        try:
            data = decode(token, key=SECRET_KEY, algorithms=["HS256"])
            user = self.db.query(Usuario).get(data["user_id"])
            if not user:
                raise HTTPException(status_code=401, detail="Token inválido")
            return user
        except exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expirado")
        except exceptions.DecodeError:
            raise HTTPException(status_code=401, detail="Token inválido")

    def revocarToken(self, token: str):
        """Revoca un token (actualmente no implementado en este ejemplo)."""
        # Aquí podríamos agregar lógica para invalidar un token almacenándolo en una lista negra.
        raise NotImplementedError("La revocación de tokens no está implementada.")

    def _validarFormatoPassword(self, password: str) -> bool:
        """Valida si una contraseña cumple con un formato seguro."""
        return len(password) >= 8 and any(c.isdigit() for c in password)

    def _encriptarPassword(self, password: str) -> str:
        """Encripta una contraseña para almacenamiento seguro."""
        return bcrypt.hash(password)

    def _correoExiste(self, email: str) -> bool:
        """Verifica si un correo ya está registrado en el sistema."""
        return self.db.query(Usuario).filter(Usuario.email == email).first() is not None

    def _crearToken(self, data: dict, expires_in_minutes: int = 60) -> str:
        """Crea un token JWT."""
        to_encode = data.copy()
        to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=expires_in_minutes)})
        return encode(payload=to_encode, key=SECRET_KEY, algorithm="HS256")
