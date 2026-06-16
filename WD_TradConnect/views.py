from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count, Q, Avg, F, FloatField
from django.db.models.functions import TruncYear, TruncMonth, TruncQuarter, TruncWeek
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import (
    FactDetallePedido, DimProducto, DimEmpresa, DimSucursal,
    DimEstadoPedido, DimTiempo
)
from .serializers import (
    StatsPedidosSerializer,
    VentasTemporalesSerializer,
    ProductoStatsSerializer,
    CategoriaRentableSerializer,
    EmpresaStatsSerializer,
    EstadoStatsSerializer,
    SegmentoPrecioSerializer,
    TopProductSerializer,
    TopEmpresaSerializer,
    TopSucursalSerializer,
)

# -------------------------------------------------------------------
# 1. ENDPOINT UNIFICADO PARA EL DASHBOARD PRINCIPAL
# -------------------------------------------------------------------
class StatsDashboardAPI(APIView):
    """
    Endpoint que devuelve todas las métricas necesarias para el dashboard.
    Combina KPIs, categorías, estados, segmentos y top productos.
    """
    permission_classes = []  # Ajusta según necesites (IsAuthenticated o público)

    @swagger_auto_schema(responses={200: StatsPedidosSerializer()})
    def get(self, request):
        # --- KPIs ---
        total_ventas = FactDetallePedido.objects.aggregate(s=Sum('total_neto'))['s'] or 0
        total_pedidos = FactDetallePedido.objects.values('pedido_id').distinct().count()
        productos_baja_rotacion = FactDetallePedido.objects.values('producto_id') \
            .annotate(total_vendido=Sum('cantidad')) \
            .filter(total_vendido__lt=10).count()
        total_productos = DimProducto.objects.count()
        ticket_promedio = total_ventas / total_pedidos if total_pedidos else 0
        porcentaje_baja = (productos_baja_rotacion / total_productos * 100) if total_productos else 0

        # --- Categorías ---
        categorias = FactDetallePedido.objects.values('producto__categoria') \
            .annotate(
                count=Count('producto_id', distinct=True),
                ventas=Sum('total_neto')
            ).order_by('-ventas')
        colors = ['#2563eb', '#f59e0b', '#8b5cf6', '#10b981', '#ef4444']
        categories_data = []
        for i, cat in enumerate(categorias):
            categories_data.append({
                'name': cat['producto__categoria'] or 'Sin categoría',
                'count': cat['count'],
                'ventas': float(cat['ventas']),
                'color': colors[i % len(colors)]
            })

        # --- Estados de pedido (adaptación de stockHealth) ---
        estados = FactDetallePedido.objects.values('estado_pedido__estado_nombre') \
            .annotate(count=Count('pedido_id', distinct=True))
        pendiente = next((e['count'] for e in estados if e['estado_pedido__estado_nombre'] == 'Pendiente'), 0)
        entregado = next((e['count'] for e in estados if e['estado_pedido__estado_nombre'] == 'Entregado'), 0)
        cancelado = next((e['count'] for e in estados if e['estado_pedido__estado_nombre'] == 'Cancelado'), 0)

        # --- Segmentos de precio ---
        productos_precio = DimProducto.objects.annotate(
            precio_prom=Sum('factdetallepedido__precio_unitario') / Count('factdetallepedido__id')
        ).filter(precio_prom__isnull=False)
        economico = productos_precio.filter(precio_prom__lt=10).count()
        estandar = productos_precio.filter(precio_prom__gte=10, precio_prom__lt=50).count()
        premium = productos_precio.filter(precio_prom__gte=50).count()

        # --- Top 10 productos por ventas ---
        top_prods = FactDetallePedido.objects.values('producto__nombre_producto', 'producto__categoria') \
            .annotate(ventas=Sum('total_neto'), pedidos=Count('pedido_id', distinct=True)) \
            .order_by('-ventas')[:10]
        top_products_data = [{
            'name': p['producto__nombre_producto'],
            'category': p['producto__categoria'] or 'General',
            'ventas': float(p['ventas']),
            'pedidos': p['pedidos']
        } for p in top_prods]

        data = {
            'summary': {
                'totalCapital': round(float(total_ventas), 2),
                'totalProducts': total_productos,
                'productsAtRisk': productos_baja_rotacion,
                'avgValue': round(ticket_promedio, 2),
                'riskPercentage': round(porcentaje_baja, 2)
            },
            'categories': categories_data,
            'stockHealth': {
                'pendiente': pendiente,
                'entregado': entregado,
                'cancelado': cancelado
            },
            'priceSegments': {
                'economico': economico,
                'estandar': estandar,
                'premium': premium
            },
            'topProducts': top_products_data
        }

        serializer = StatsPedidosSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


# -------------------------------------------------------------------
# 2. ANÁLISIS TEMPORAL
# -------------------------------------------------------------------
class VentasTemporalesAPI(APIView):
    """
    Ventas totales agrupadas por año, mes, trimestre o semana.
    Parámetros opcionales: 'periodo' (year, month, quarter, week) y 'fecha_inicio', 'fecha_fin'.
    """
    permission_classes = []

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('periodo', openapi.IN_QUERY, type=openapi.TYPE_STRING, enum=['year', 'month', 'quarter', 'week']),
            openapi.Parameter('fecha_inicio', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='date'),
            openapi.Parameter('fecha_fin', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='date'),
        ],
        responses={200: VentasTemporalesSerializer(many=True)}
    )
    def get(self, request):
        periodo = request.query_params.get('periodo', 'month')
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')

        queryset = FactDetallePedido.objects.all()

        if fecha_inicio:
            queryset = queryset.filter(fecha__fecha__gte=fecha_inicio)
        if fecha_fin:
            queryset = queryset.filter(fecha__fecha__lte=fecha_fin)

        # Mapeo de período a función de truncado
        trunc_fn = {
            'year': TruncYear('fecha__fecha'),
            'quarter': TruncQuarter('fecha__fecha'),
            'month': TruncMonth('fecha__fecha'),
            'week': TruncWeek('fecha__fecha'),
        }.get(periodo, TruncMonth('fecha__fecha'))

        ventas = queryset.annotate(periodo=trunc_fn) \
            .values('periodo') \
            .annotate(
                total_ventas=Sum('total_neto'),
                total_pedidos=Count('pedido_id', distinct=True),
                total_unidades=Sum('cantidad')
            ).order_by('periodo')

        result = []
        for v in ventas:
            result.append({
                'periodo': v['periodo'].strftime('%Y-%m-%d') if hasattr(v['periodo'], 'strftime') else str(v['periodo']),
                'total_ventas': float(v['total_ventas'] or 0),
                'total_pedidos': v['total_pedidos'],
                'total_unidades': float(v['total_unidades'] or 0),
            })

        return Response(result)


# -------------------------------------------------------------------
# 3. ANÁLISIS POR PRODUCTOS
# -------------------------------------------------------------------
class ProductosTopAPI(APIView):
    """Top productos por ingresos y por unidades vendidas"""
    permission_classes = []

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('orden', openapi.IN_QUERY, type=openapi.TYPE_STRING, enum=['ventas', 'unidades']),
            openapi.Parameter('limite', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
        responses={200: ProductoStatsSerializer(many=True)}
    )
    def get(self, request):
        orden = request.query_params.get('orden', 'ventas')
        limite = int(request.query_params.get('limite', 10))

        orden_map = {
            'ventas': '-total_ventas',
            'unidades': '-total_unidades'
        }
        order_by = orden_map.get(orden, '-total_ventas')

        productos = FactDetallePedido.objects.values(
            'producto_id', 'producto__nombre_producto', 'producto__categoria'
        ).annotate(
            total_ventas=Sum('total_neto'),
            total_unidades=Sum('cantidad'),
            pedidos=Count('pedido_id', distinct=True)
        ).order_by(order_by)[:limite]

        data = [{
            'producto_id': p['producto_id'],
            'nombre': p['producto__nombre_producto'],
            'categoria': p['producto__categoria'],
            'total_ventas': float(p['total_ventas'] or 0),
            'total_unidades': float(p['total_unidades'] or 0),
            'pedidos': p['pedidos'],
        } for p in productos]

        return Response(data)


class CategoriasRentablesAPI(APIView):
    """Categorías más rentables (por total de ventas)"""
    permission_classes = []

    @swagger_auto_schema(responses={200: CategoriaRentableSerializer(many=True)})
    def get(self, request):
        categorias = FactDetallePedido.objects.values('producto__categoria') \
            .annotate(
                ventas=Sum('total_neto'),
                productos=Count('producto_id', distinct=True),
                unidades=Sum('cantidad')
            ).order_by('-ventas')

        data = [{
            'categoria': c['producto__categoria'] or 'Sin categoría',
            'ventas': float(c['ventas'] or 0),
            'productos': c['productos'],
            'unidades': float(c['unidades'] or 0),
        } for c in categorias]

        return Response(data)


# -------------------------------------------------------------------
# 4. ANÁLISIS POR CLIENTES (EMPRESAS)
# -------------------------------------------------------------------
class EmpresasTopAPI(APIView):
    """Top empresas por facturación y pedidos"""
    permission_classes = []

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('orden', openapi.IN_QUERY, type=openapi.TYPE_STRING, enum=['facturacion', 'pedidos']),
            openapi.Parameter('limite', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
        responses={200: EmpresaStatsSerializer(many=True)}
    )
    def get(self, request):
        orden = request.query_params.get('orden', 'facturacion')
        limite = int(request.query_params.get('limite', 5))

        orden_map = {
            'facturacion': '-total_facturado',
            'pedidos': '-total_pedidos'
        }
        order_by = orden_map.get(orden, '-total_facturado')

        empresas = FactDetallePedido.objects.values(
            'empresa_id', 'empresa__razon_social', 'empresa__ruc'
        ).annotate(
            total_facturado=Sum('total_neto'),
            total_pedidos=Count('pedido_id', distinct=True),
            ticket_promedio=Sum('total_neto') / Count('pedido_id', distinct=True)
        ).order_by(order_by)[:limite]

        data = [{
            'empresa_id': e['empresa_id'],
            'razon_social': e['empresa__razon_social'],
            'ruc': e['empresa__ruc'],
            'total_facturado': float(e['total_facturado'] or 0),
            'total_pedidos': e['total_pedidos'],
            'ticket_promedio': round(float(e['ticket_promedio'] or 0), 2),
        } for e in empresas]

        return Response(data)


class SucursalesTopAPI(APIView):
    """Top sucursales por pedidos"""
    permission_classes = []

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('empresa_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
            openapi.Parameter('limite', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        ],
        responses={200: TopSucursalSerializer(many=True)}
    )
    def get(self, request):
        empresa_id = request.query_params.get('empresa_id')
        limite = int(request.query_params.get('limite', 5))

        queryset = FactDetallePedido.objects.values(
            'sucursal_id', 'sucursal__nombre_lugar', 'sucursal__municipio'
        ).annotate(
            total_pedidos=Count('pedido_id', distinct=True),
            total_facturado=Sum('total_neto')
        )
        if empresa_id:
            queryset = queryset.filter(empresa_id=empresa_id)

        sucursales = queryset.order_by('-total_pedidos')[:limite]

        data = [{
            'sucursal_id': s['sucursal_id'],
            'nombre': s['sucursal__nombre_lugar'],
            'municipio': s['sucursal__municipio'],
            'total_pedidos': s['total_pedidos'],
            'total_facturado': float(s['total_facturado'] or 0),
        } for s in sucursales]

        return Response(data)


# -------------------------------------------------------------------
# 5. ANÁLISIS POR ESTADO DEL PEDIDO
# -------------------------------------------------------------------
class EstadosAPI(APIView):
    """Distribución y valor por estado de pedido"""
    permission_classes = []

    @swagger_auto_schema(responses={200: EstadoStatsSerializer(many=True)})
    def get(self, request):
        estados = FactDetallePedido.objects.values('estado_pedido__estado_nombre') \
            .annotate(
                count=Count('pedido_id', distinct=True),
                valor_total=Sum('total_neto')
            )
        data = [{
            'estado': e['estado_pedido__estado_nombre'],
            'cantidad_pedidos': e['count'],
            'valor_total': float(e['valor_total'] or 0),
        } for e in estados]

        return Response(data)


# -------------------------------------------------------------------
# 6. SEGMENTACIÓN POR PRECIO
# -------------------------------------------------------------------
class SegmentacionPrecioAPI(APIView):
    """Cuenta de productos según segmento de precio unitario promedio"""
    permission_classes = []

    @swagger_auto_schema(responses={200: SegmentoPrecioSerializer(many=True)})
    def get(self, request):
        # Obtener el precio promedio real de cada producto a partir de los pedidos
        productos = DimProducto.objects.annotate(
            precio_prom=Sum('factdetallepedido__precio_unitario') / Count('factdetallepedido__id')
        ).filter(precio_prom__isnull=False)

        segmentos = [
            {'segmento': 'Económico', 'min': 0, 'max': 10},
            {'segmento': 'Estándar', 'min': 10, 'max': 50},
            {'segmento': 'Premium', 'min': 50, 'max': None},
        ]

        data = []
        for seg in segmentos:
            qs = productos
            if seg['max'] is not None:
                qs = qs.filter(precio_prom__gte=seg['min'], precio_prom__lt=seg['max'])
            else:
                qs = qs.filter(precio_prom__gte=seg['min'])
            data.append({
                'segmento': seg['segmento'],
                'cantidad_productos': qs.count(),
            })

        return Response(data)


# -------------------------------------------------------------------
# 7. RANKINGS (TOP N)
# -------------------------------------------------------------------
class RankingsAPI(APIView):
    """Combina top 10 productos, top 5 empresas y top 5 sucursales en un solo endpoint"""
    permission_classes = []

    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description="Rankings combinados",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'top_productos': openapi.Schema(type=openapi.TYPE_ARRAY, items=TopProductSerializer),
                        'top_empresas': openapi.Schema(type=openapi.TYPE_ARRAY, items=TopEmpresaSerializer),
                        'top_sucursales': openapi.Schema(type=openapi.TYPE_ARRAY, items=TopSucursalSerializer),
                    }
                )
            )
        }
    )
    def get(self, request):
        # Top 10 productos
        top_prods = FactDetallePedido.objects.values('producto__nombre_producto', 'producto__categoria') \
            .annotate(ventas=Sum('total_neto')) \
            .order_by('-ventas')[:10]
        productos_list = [{
            'name': p['producto__nombre_producto'],
            'category': p['producto__categoria'] or 'General',
            'ventas': float(p['ventas']),
            'pedidos': 0  # podría agregarse con otro annotate
        } for p in top_prods]

        # Top 5 empresas
        empresas = FactDetallePedido.objects.values('empresa__razon_social', 'empresa__ruc') \
            .annotate(total_facturado=Sum('total_neto'), pedidos=Count('pedido_id', distinct=True)) \
            .order_by('-total_facturado')[:5]
        empresas_list = [{
            'razon_social': e['empresa__razon_social'],
            'ruc': e['empresa__ruc'],
            'total_facturado': float(e['total_facturado']),
            'total_pedidos': e['pedidos'],
        } for e in empresas]

        # Top 5 sucursales
        sucursales = FactDetallePedido.objects.values('sucursal__nombre_lugar') \
            .annotate(total_pedidos=Count('pedido_id', distinct=True)) \
            .order_by('-total_pedidos')[:5]
        sucursales_list = [{
            'nombre': s['sucursal__nombre_lugar'],
            'total_pedidos': s['total_pedidos'],
        } for s in sucursales]

        data = {
            'top_productos': productos_list,
            'top_empresas': empresas_list,
            'top_sucursales': sucursales_list,
        }
        return Response(data)