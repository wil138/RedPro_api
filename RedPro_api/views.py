from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication # 🔑 Necesario para el 401
from .models import (
    Categoria, Estadoproducto, Estadopedido, Metodopago,
    Clientes, Proveedor, Productos, Pedido, Factura, Establecimientos,
    Usuario
)
from .serializers import (
    CategoriaSerializer, EstadoProductoSerializer, EstadoPedidoSerializer, MetodoPagoSerializer,
    ClienteSerializer, ClienteCreationSerializer,
    ProveedorSerializer, ProductoSerializer, PedidoSerializer, FacturaSerializer,
    EstablecimientoSerializer, UserCreationSerializer
)
from drf_yasg.utils import swagger_auto_schema

# --- Configuración de Seguridad Base (Recomendada) ---

# Usamos JWTAuthentication para todas las vistas protegidas
DEFAULT_AUTH = [JWTAuthentication]
# Requerimos que el usuario esté autenticado para todas las vistas CRUD por defecto
DEFAULT_PERMS = [IsAuthenticated]


# --- ViewSet para Usuarios ---
class UserViewSet(viewsets.ModelViewSet):
    """CRUD para usuarios (perfiles). Requiere autenticación."""
    queryset = User.objects.all()
    serializer_class = UserCreationSerializer
    
   


# --- ViewSets de Tablas de Lookup ---
class CategoriaViewSet(viewsets.ModelViewSet):
    """CRUD para categorías de productos."""
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer



class EstadoProductoViewSet(viewsets.ModelViewSet):
    """CRUD para estados de productos (Disponible, Agotado, etc.)."""
    queryset = Estadoproducto.objects.all()
    serializer_class = EstadoProductoSerializer
 


class EstadoPedidoViewSet(viewsets.ModelViewSet):
    """CRUD para estados de pedidos (Pendiente, Enviado, Entregado, etc.)."""
    queryset = Estadopedido.objects.all()
    serializer_class = EstadoPedidoSerializer
 


class MetodoPagoViewSet(viewsets.ModelViewSet):
    """CRUD para métodos de pago (Efectivo, Tarjeta, etc.)."""
    queryset = Metodopago.objects.all()
    serializer_class = MetodoPagoSerializer
    


# --- ViewSets para Entidades Principales (Protegidas) ---

class ProveedorViewSet(viewsets.ModelViewSet):
    """CRUD para la gestión de proveedores."""
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
 


class ProductoViewSet(viewsets.ModelViewSet):
    """CRUD para la gestión de productos."""
    queryset = Productos.objects.all()
    serializer_class = ProductoSerializer
  


class EstablecimientoViewSet(viewsets.ModelViewSet):
    """CRUD para la gestión de establecimientos."""
    queryset = Establecimientos.objects.all()
    serializer_class = EstablecimientoSerializer
  


class PedidoViewSet(viewsets.ModelViewSet):
    """CRUD para la gestión de pedidos."""
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
   


class FacturaViewSet(viewsets.ModelViewSet):
    """CRUD para la gestión de facturas/detalles de pedido."""
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer
   


# --- ViewSet para Clientes (Permisos Condicionales) ---

class ClienteViewSet(viewsets.ModelViewSet):
    """
    CRUD para clientes.
    Permite el registro (POST) sin autenticación. 
    Las demás operaciones requieren autenticación.
    """
    queryset = Clientes.objects.all()
    serializer_class = ClienteSerializer
    

    def get_serializer_class(self):
        """Usa ClienteCreationSerializer solo para la creación (POST)."""
        if self.request.method == 'POST':
            return ClienteCreationSerializer
        return ClienteSerializer

    def get_permissions(self):
        """Define permisos basados en la acción."""
        # 🔓 Permite la creación (POST) sin autenticación
        if self.action == 'create':
            return [AllowAny()]
        
        # 🔒 Requiere autenticación (Token JWT) para GET, PUT, DELETE, etc.
        return [IsAuthenticated()]

@swagger_auto_schema(auto_schema=None)
class ProblematicViewSet(viewsets.ModelViewSet):
    ...