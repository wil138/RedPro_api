from django.urls import path
from . import views

urlpatterns = [
    # Dashboard principal
    path('stats/', views.StatsDashboardAPI.as_view(), name='api-stats'),
    # Análisis temporal
    path('ventas-temporales/', views.VentasTemporalesAPI.as_view(), name='ventas-temporales'),
    # Productos
    path('productos/top/', views.ProductosTopAPI.as_view(), name='productos-top'),
    path('categorias/rentables/', views.CategoriasRentablesAPI.as_view(), name='categorias-rentables'),
    # Clientes
    path('empresas/top/', views.EmpresasTopAPI.as_view(), name='empresas-top'),
    path('sucursales/top/', views.SucursalesTopAPI.as_view(), name='sucursales-top'),
    # Estados de pedido
    path('estados/', views.EstadosAPI.as_view(), name='estados-pedido'),
    # Segmentación precio
    path('segmentacion-precio/', views.SegmentacionPrecioAPI.as_view(), name='segmentacion-precio'),
    # Rankings combinados
    path('rankings/', views.RankingsAPI.as_view(), name='rankings'),
]