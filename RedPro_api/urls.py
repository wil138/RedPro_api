from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Crea una instancia de DefaultRouter
# El Router registrará automáticamente las rutas para los ViewSets
router = DefaultRouter()

# --- Registro de ViewSets Principales ---
router.register(r'usuarios', views.UserViewSet, basename='usuario')
# /clientes/ y /clientes/{pk}/
router.register(r'clientes', views.ClienteViewSet, basename='cliente')
# /proveedores/ y /proveedores/{pk}/
router.register(r'proveedores', views.ProveedorViewSet, basename='proveedor')
# /productos/ y /productos/{pk}/
router.register(r'productos', views.ProductoViewSet, basename='producto')
# /establecimientos/ y /establecimientos/{pk}/
router.register(r'establecimientos', views.EstablecimientoViewSet, basename='establecimiento')
# /pedidos/ y /pedidos/{pk}/
router.register(r'pedidos', views.PedidoViewSet, basename='pedido')
# /facturas/ y /facturas/{pk}/
router.register(r'facturas', views.FacturaViewSet, basename='factura')


# --- Registro de ViewSets de Tablas de Lookup ---
# /categorias/
router.register(r'categorias', views.CategoriaViewSet, basename='categoria')
# /estados/producto/
router.register(r'estados/producto', views.EstadoProductoViewSet, basename='estadoproducto')
# /estados/pedido/
router.register(r'estados/pedido', views.EstadoPedidoViewSet, basename='estadopedido')
# /metodos/pago/
router.register(r'metodos/pago', views.MetodoPagoViewSet, basename='metodopago')


# La lista de URLs que se generan automáticamente
urlpatterns = [
    # Incluye todas las rutas generadas por el Router
    path('', include(router.urls)),
]