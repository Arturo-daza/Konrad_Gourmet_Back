from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.database import DatabaseManager
from .routes.administracion import router as user_router
from .routes.inventarios import router as inventario_router
from .routes.platos import router as plato_router
from .routes.pedidos import router as pedido_router
from .routes.auth import router as auth_router
from .routes.productos import router as producto_router
from .routes.categorias import router as categoria_router
from .middlewares.error_handler import ErrorHandler

# Crear instancia de FastAPI
app = FastAPI(
    title="Konrad Gourmet API",
    description="API para gestionar platos, pedidos, inventarios, usuarios y más.",
    version="1.0.0"
)

# Middleware de CORS
origins = ["*"]  # Cambiar "*" por dominios específicos para mayor seguridad
app.add_middleware(ErrorHandler)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conectar base de datos
db_instance = DatabaseManager.get_instance()

# Registrar Rutas
app.include_router(plato_router, prefix="/api/platos", tags=["Platos"])
app.include_router(pedido_router, prefix="/api/pedidos", tags=["Pedidos"])
app.include_router(inventario_router, prefix="/api/inventarios", tags=["Inventarios"])
app.include_router(user_router, prefix="/api/usuarios", tags=["Usuarios"])
app.include_router(auth_router, prefix="/api/auth", tags=["Autenticación"])
app.include_router(producto_router, prefix="/api/productos", tags=["Productos"])
app.include_router(categoria_router, prefix="/api/categorias", tags=["categorias"])



# Root Endpoint
@app.get("/", tags=["Root"])
async def root():
    return {"message": "¡Bienvenido a la API del Sistema de Restaurante!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
