from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

# --- Registro de ViewSets Principales ---
router.register(r'usuarios', views.UserViewSet, basename='usuario')
router.register(r'clientes', views.ClienteViewSet, basename='cliente')
router.register(r'proveedores', views.ProveedorViewSet, basename='proveedor')
router.register(r'productos', views.ProductoViewSet, basename='producto')
router.register(r'establecimientos', views.EstablecimientoViewSet, basename='establecimiento')
router.register(r'pedidos', views.PedidoViewSet, basename='pedido')
router.register(r'facturas', views.FacturaViewSet, basename='factura')

# --- Registro de ViewSets de Tablas de Lookup ---
router.register(r'categorias', views.CategoriaViewSet, basename='categoria')
router.register(r'estados/producto', views.EstadoProductoViewSet, basename='estadoproducto')
router.register(r'estados/pedido', views.EstadoPedidoViewSet, basename='estadopedido')
router.register(r'metodos/pago', views.MetodoPagoViewSet, basename='metodopago')

# ✅ Forma correcta de exponer las rutas
urlpatterns = [
    path('', include(router.urls)),
]