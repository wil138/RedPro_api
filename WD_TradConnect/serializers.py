from rest_framework import serializers

# -------------------------------------------------------------------
# Serializadores para el dashboard principal
# -------------------------------------------------------------------
class SummarySerializer(serializers.Serializer):
    """KPIs principales del dashboard"""
    totalCapital = serializers.FloatField(help_text="Ventas totales (Total Neto)")
    totalProducts = serializers.IntegerField(help_text="Número de productos distintos")
    productsAtRisk = serializers.IntegerField(help_text="Productos con baja rotación (<10 ventas)")
    avgValue = serializers.FloatField(help_text="Ticket promedio")
    riskPercentage = serializers.FloatField(help_text="Porcentaje de productos en riesgo")


class CategoryStatSerializer(serializers.Serializer):
    """Estadísticas por categoría de producto"""
    name = serializers.CharField(help_text="Nombre de la categoría")
    count = serializers.IntegerField(help_text="Cantidad de productos distintos en la categoría")
    ventas = serializers.FloatField(help_text="Total de ventas de la categoría")
    color = serializers.CharField(help_text="Color hexadecimal para la gráfica")


class EstadoPedidoStatSerializer(serializers.Serializer):
    """Distribución de estados de pedido (adaptación de stockHealth)"""
    pendiente = serializers.IntegerField()
    entregado = serializers.IntegerField()
    cancelado = serializers.IntegerField()


class PriceSegmentSerializer(serializers.Serializer):
    """Segmentos de precio unitario"""
    economico = serializers.IntegerField()
    estandar = serializers.IntegerField()
    premium = serializers.IntegerField()


class TopProductSerializer(serializers.Serializer):
    """Producto en el top 10 de ventas"""
    name = serializers.CharField(help_text="Nombre del producto")
    category = serializers.CharField(help_text="Categoría del producto")
    ventas = serializers.FloatField(help_text="Total vendido ($)")
    pedidos = serializers.IntegerField(help_text="Número de pedidos que lo incluyen")


class StatsPedidosSerializer(serializers.Serializer):
    """Respuesta completa del endpoint de estadísticas"""
    summary = SummarySerializer(help_text="Indicadores clave de rendimiento")
    categories = CategoryStatSerializer(many=True, help_text="Ventas por categoría")
    stockHealth = EstadoPedidoStatSerializer(help_text="Distribución de estados de pedido")
    priceSegments = PriceSegmentSerializer(help_text="Segmentación de precios")
    topProducts = TopProductSerializer(many=True, help_text="Top 10 productos por ventas")


# -------------------------------------------------------------------
# Serializadores para los demás endpoints
# -------------------------------------------------------------------
class VentasTemporalesSerializer(serializers.Serializer):
    periodo = serializers.CharField()
    total_ventas = serializers.FloatField()
    total_pedidos = serializers.IntegerField()
    total_unidades = serializers.FloatField()


class ProductoStatsSerializer(serializers.Serializer):
    producto_id = serializers.IntegerField()
    nombre = serializers.CharField()
    categoria = serializers.CharField()
    total_ventas = serializers.FloatField()
    total_unidades = serializers.FloatField()
    pedidos = serializers.IntegerField()


class CategoriaRentableSerializer(serializers.Serializer):
    categoria = serializers.CharField()
    ventas = serializers.FloatField()
    productos = serializers.IntegerField()
    unidades = serializers.FloatField()


class EmpresaStatsSerializer(serializers.Serializer):
    empresa_id = serializers.IntegerField()
    razon_social = serializers.CharField()
    ruc = serializers.CharField()
    total_facturado = serializers.FloatField()
    total_pedidos = serializers.IntegerField()
    ticket_promedio = serializers.FloatField()


class TopEmpresaSerializer(serializers.Serializer):
    razon_social = serializers.CharField()
    ruc = serializers.CharField()
    total_facturado = serializers.FloatField()
    total_pedidos = serializers.IntegerField()


class TopSucursalSerializer(serializers.Serializer):
    sucursal_id = serializers.IntegerField(required=False)
    nombre = serializers.CharField()
    municipio = serializers.CharField(required=False)
    total_pedidos = serializers.IntegerField()
    total_facturado = serializers.FloatField(required=False)


class EstadoStatsSerializer(serializers.Serializer):
    estado = serializers.CharField()
    cantidad_pedidos = serializers.IntegerField()
    valor_total = serializers.FloatField()


class SegmentoPrecioSerializer(serializers.Serializer):
    segmento = serializers.CharField()
    cantidad_productos = serializers.IntegerField()