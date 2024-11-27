from .auth_schema import Token
from .user_schema import UsuarioCreate, UsuarioResponse, RolBase
from .inventario_schema import InventarioBase, InventarioUpdate, InventarioResponse, InventarioCreate, ProductoDetalle, InventarioDetalleResponse
from .pedido_schema import PedidoCreate, PedidoResponse, PedidoUpdate, PedidoDetalleResponse
from .plato_schema import PlatoCreate, PlatoResponse, PlatoUpdate, PlatoPreparadoResponse
from .producto_schema import ProductoBase, ProductoCreate, ProductoResponse, ProductoIDs
from .categoria_schema import CategoriaBase, CategoriaCreate, CategoriaResponse