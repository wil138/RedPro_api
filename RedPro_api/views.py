from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
# Importar los modelos corregidos
from .models import (
    Categoria, Estadoproducto, Estadopedido, Metodopago,
    Clientes, Proveedor, Productos, Pedido, Factura, Establecimientos  # <-- ¡Establecimiento añadido aquí!
)
# Asumiendo que has creado los serializadores correspondientes
from .serializers import (
    CategoriaSerializer, EstadoProductoSerializer, EstadoPedidoSerializer, MetodoPagoSerializer,
    ClienteSerializer, ClienteCreationSerializer,
    ProveedorSerializer, ProductoSerializer, PedidoSerializer, FacturaSerializer,
    EstablecimientoSerializer  # <-- ¡EstablecimientoSerializer añadido aquí!
)


# --- ViewSets para Tablas de Lookup (Requieren Autenticación para CRUD) ---
class UserViewSet(viewsets.ModelViewSet):
    """CRUD para usuarios (perfiles)."""
    from django.contrib.auth.models import User
    from .serializers import UserCreationSerializer

    queryset = User.objects.all()
    serializer_class = UserCreationSerializer
    permission_classes = [IsAuthenticated]

class CategoriaViewSet(viewsets.ModelViewSet):
    """CRUD para categorías de productos."""
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated]


class EstadoProductoViewSet(viewsets.ModelViewSet):
    """CRUD para estados de productos (Disponible, Agotado, etc.)."""
    queryset = Estadoproducto.objects.all()
    serializer_class = EstadoProductoSerializer
    permission_classes = [IsAuthenticated]


class EstadoPedidoViewSet(viewsets.ModelViewSet):
    """CRUD para estados de pedidos (Pendiente, Enviado, Entregado, etc.)."""
    queryset = Estadopedido.objects.all()
    serializer_class = EstadoPedidoSerializer
    permission_classes = [IsAuthenticated]


class MetodoPagoViewSet(viewsets.ModelViewSet):
    """CRUD para métodos de pago (Efectivo, Tarjeta, etc.)."""
    queryset = Metodopago.objects.all()
    serializer_class = MetodoPagoSerializer
    permission_classes = [IsAuthenticated]


# --- ViewSets para Entidades Principales ---

class ProveedorViewSet(viewsets.ModelViewSet):
    """CRUD para la gestión de proveedores."""
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer
    permission_classes = [IsAuthenticated]


class ProductoViewSet(viewsets.ModelViewSet):
    """CRUD para la gestión de productos."""
    queryset = Productos.objects.all()
    serializer_class = ProductoSerializer
    permission_classes = [IsAuthenticated]


# 🆕 ViewSet para Establecimientos
class EstablecimientoViewSet(viewsets.ModelViewSet):
    """CRUD para la gestión de establecimientos."""
    queryset = Establecimientos.objects.all()
    serializer_class = EstablecimientoSerializer
    permission_classes = [IsAuthenticated]  # Requiere autenticación


class PedidoViewSet(viewsets.ModelViewSet):
    """CRUD para la gestión de pedidos."""
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]


class FacturaViewSet(viewsets.ModelViewSet):
    """CRUD para la gestión de facturas/detalles de pedido."""
    queryset = Factura.objects.all()
    serializer_class = FacturaSerializer
    permission_classes = [IsAuthenticated]


# --- ViewSet para Clientes (con Permisos Condicionales para Registro) ---

class ClienteViewSet(viewsets.ModelViewSet):
    """
    CRUD para clientes.
    Permite el registro (POST/create) sin autenticación (registro abierto).
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
        if self.action == 'create':
            return [AllowAny()]

        return [IsAuthenticated()]