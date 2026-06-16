from django.db import models

class DimTiempo(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    fecha = models.DateField(db_column='Fecha')
    anio = models.IntegerField(db_column='Año')
    mes = models.IntegerField(db_column='Mes')
    dia = models.IntegerField(db_column='Dia')
    trimestre = models.IntegerField(db_column='Trimestre')
    semana = models.IntegerField(db_column='Semana')

    class Meta:
        managed = False
        db_table = 'DimTiempo'
        app_label = 'analytics'


class DimEmpresa(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    empresa_id = models.IntegerField(db_column='Empresa_Id')
    razon_social = models.CharField(max_length=150, db_column='RazonSocial')
    ruc = models.CharField(max_length=50, db_column='RUC')

    class Meta:
        managed = False
        db_table = 'DimEmpresa'
        app_label = 'analytics'


class DimSucursal(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    sucursal_id = models.IntegerField(db_column='Sucursal_Id')
    nombre_lugar = models.CharField(max_length=150, db_column='NombreLugar')
    municipio = models.CharField(max_length=100, null=True, blank=True, db_column='Municipio')
    direccion_exacta = models.CharField(max_length=250, null=True, blank=True, db_column='DireccionExacta')

    class Meta:
        managed = False
        db_table = 'DimSucursal'
        app_label = 'analytics'


class DimProducto(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    producto_id = models.IntegerField(db_column='Producto_Id')
    nombre_producto = models.CharField(max_length=150, db_column='NombreProducto')
    categoria = models.CharField(max_length=100, null=True, blank=True, db_column='Categoria')
    unidad_medida = models.CharField(max_length=50, null=True, blank=True, db_column='UnidadMedida')

    class Meta:
        managed = False
        db_table = 'DimProducto'
        app_label = 'analytics'


class DimEstadoPedido(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    estado_id = models.IntegerField(db_column='Estado_Id')
    estado_nombre = models.CharField(max_length=50, db_column='EstadoNombre')

    class Meta:
        managed = False
        db_table = 'DimEstadoPedido'
        app_label = 'analytics'


class FactDetallePedido(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    pedido_id = models.IntegerField(db_column='PedidoId')

    # Foreign keys a las dimensiones
    producto = models.ForeignKey(
        DimProducto,
        on_delete=models.DO_NOTHING,
        db_column='ProductoId'
    )
    empresa = models.ForeignKey(
        DimEmpresa,
        on_delete=models.DO_NOTHING,
        db_column='EmpresaId'
    )
    sucursal = models.ForeignKey(
        DimSucursal,
        on_delete=models.DO_NOTHING,
        db_column='SucursalId'
    )
    fecha = models.ForeignKey(
        DimTiempo,
        on_delete=models.DO_NOTHING,
        db_column='FechaId'
    )
    estado_pedido = models.ForeignKey(
        DimEstadoPedido,
        on_delete=models.DO_NOTHING,
        db_column='EstadoPedidoId'
    )

    # Métricas
    cantidad = models.DecimalField(max_digits=12, decimal_places=2, db_column='Cantidad')
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, db_column='PrecioUnitario')
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0, db_column='Descuento')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, db_column='Subtotal')
    total_neto = models.DecimalField(max_digits=12, decimal_places=2, db_column='TotalNeto')

    class Meta:
        managed = False
        db_table = 'FactDetallePedido'
        app_label = 'analytics'