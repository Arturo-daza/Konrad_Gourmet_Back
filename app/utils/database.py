from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base

# Carga las variables de entorno desde .env
load_dotenv()

# Obtiene la URL de la base de datos desde las variables de entorno, eliminando el parámetro ssl-mode
DATABASE_URL = os.getenv("DATABASE_URL").replace('?ssl-mode=REQUIRED', '')

# Configura los argumentos para SSL si es necesario
ssl_args = {
    "ssl": {
        "ssl": "true"  # Ruta al certificado CA si es necesario
    }
}

Base = declarative_base()


class DatabaseManager:
    __instance = None

    def __init__(self):
        if DatabaseManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            try:
                # Inicializa la conexión con la base de datos
                self.connection = create_engine(DATABASE_URL, connect_args=ssl_args)
                # Configura el SessionLocal
                self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.connection)
                DatabaseManager.__instance = self
            except SQLAlchemyError as e:
                raise ConnectionError(f"Error connecting to the database: {str(e)}")

    @staticmethod
    def get_instance():
        if DatabaseManager.__instance is None:
            DatabaseManager()
        return DatabaseManager.__instance

    def get_connection(self):
        return self.connection

    def realizar_backup(self, backup_path: str):
        """Realiza un backup de la base de datos."""
        try:
            with self.connection.connect() as conn:
                backup_query = f"BACKUP DATABASE TO DISK='{backup_path}'"
                conn.execute(text(backup_query))
            print(f"Backup realizado exitosamente en: {backup_path}")
        except SQLAlchemyError as e:
            raise Exception(f"Error realizando backup: {str(e)}")

    def restaurar_backup(self, backup_path: str):
        """Restaura la base de datos desde un backup."""
        try:
            with self.connection.connect() as conn:
                restore_query = f"RESTORE DATABASE FROM DISK='{backup_path}'"
                conn.execute(text(restore_query))
            print(f"Base de datos restaurada exitosamente desde: {backup_path}")
        except SQLAlchemyError as e:
            raise Exception(f"Error restaurando backup: {str(e)}")