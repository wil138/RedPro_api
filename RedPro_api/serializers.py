from rest_framework import serializers
from django.contrib.auth.models import User
# Importamos los modelos
from .models import (
    Categoria, Estadopedido, Estadoproducto, Metodopago,
    Clientes, Proveedor, Productos, Pedido, Factura, Establecimientos
)


# =========================================================
# I. Serializadores para Tablas de Lookup (Nivel 1)
# =========================================================

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class EstadoPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estadopedido
        fields = '__all__'


class EstadoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estadoproducto
        fields = '__all__'


class MetodoPagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metodopago
        fields = '__all__'

# =========================================================
# II. Serializadores de Entidades (Nivel 2)
# =========================================================

# --- Serializador Básico de Usuario (Perfil/Creación) ---
class UserCreationSerializer(serializers.ModelSerializer):
    """Serializador para crear un nuevo usuario (registro)."""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True},
        }

    def create(self, validated_data):
        # Usamos create_user para garantizar el hasheo de la contraseña
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


# --- Proveedor ---
class ProveedorSerializer(serializers.ModelSerializer):
    # ASUNCIÓN: El campo FK en Proveedor hacia User es 'usuario'.
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Proveedor
        fields = '__all__'
        read_only_fields = ('id', 'usuario_username')


# --- Producto ---
class ProductoSerializer(serializers.ModelSerializer):
    # Campos de Lectura (Anidados para mostrar el objeto completo)
    # ASUNCIÓN: Los campos FK son 'proveedorid', 'estadoid', 'categoriaid'.
    proveedor_nombre = serializers.CharField(source='proveedorid.nombre', read_only=True)
    estado = EstadoProductoSerializer(read_only=True) 
    categoria = CategoriaSerializer(read_only=True)   

    # Campos de Escritura (Para enviar solo el ID en el POST/PUT)
    estadoproductoid = serializers.PrimaryKeyRelatedField(queryset=Estadoproducto.objects.all(), write_only=True)
    categoriaid = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all(), write_only=True)

    class Meta:
        model = Productos
        fields = (
            'id', 'codigoproducto', 'nombre', 'descripcion', 'cantidad', 'imagen', 'precio', 'fechacreacion',
            
            # IDs de las Foreign Keys para escritura/actualización
            'proveedorid', 'estadoproductoid', 'categoriaid', 
            
            # Campos anidados/nombres de las FK para lectura
            'proveedor_nombre', 'estado', 'categoria', 
        )
        read_only_fields = (
            'id', 'fechacreacion', 'proveedor_nombre', 
        )


# --- Cliente (Para Listar/Leer/Actualizar) ---
class ClienteSerializer(serializers.ModelSerializer):
    usuario_nombreusuario = serializers.CharField(source='usuarioid.nombreusuario', read_only=True)

    class Meta:
        model = Clientes
        fields = '__all__'
        read_only_fields = ('id', 'usuario_nombreusuario')


# --- Cliente (Para Registro Abierto: Creación/POST) ---
class ClienteCreationSerializer(serializers.ModelSerializer):
    usuario = UserCreationSerializer(write_only=True)

    class Meta:
        model = Clientes
        fields = ('numeroruc', 'nombre', 'apellido', 'telefono', 'usuario')

    def create(self, validated_data):
        user_data = validated_data.pop('usuario')
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        # Asumiendo que el campo FK en Clientes a User se llama 'usuario'
        cliente = Clientes.objects.create(usuario=user, **validated_data)
        return cliente


# --- Establecimiento ---
class EstablecimientoSerializer(serializers.ModelSerializer):
    # ASUNCIÓN: El campo FK en Establecimientos hacia User es 'usuarioid'.
    usuario_username = serializers.CharField(source='usuarioid.username', read_only=True)

    class Meta:
        model = Establecimientos
        fields = '__all__'
        read_only_fields = ('id', 'usuario_username')


# --- Pedido (CORREGIDO para seguridad y claridad) ---
class PedidoSerializer(serializers.ModelSerializer):
    cliente_nombre = serializers.CharField(source='clienteid.nombre', read_only=True)
    estado_pedido_nombre = serializers.CharField(source='estadopedidoid.estadopedido', read_only=True)
    metodo_pago_nombre = serializers.CharField(source='metodopagoid.nombremetodo', read_only=True)

    clienteid = serializers.PrimaryKeyRelatedField(queryset=Clientes.objects.all(), write_only=True)
    estadopedidoid = serializers.PrimaryKeyRelatedField(queryset=Estadopedido.objects.all(), write_only=True)
    metodopagoid = serializers.PrimaryKeyRelatedField(queryset=Metodopago.objects.all(), write_only=True)

    class Meta:
        model = Pedido
        fields = (
            'id', 'codigopedido', 'fechapedido', 'total',
            'clienteid', 'estadopedidoid', 'metodopagoid',
            'cliente_nombre', 'estado_pedido_nombre', 'metodo_pago_nombre',
        )
        read_only_fields = ('id', 'cliente_nombre', 'estado_pedido_nombre', 'metodo_pago_nombre')


# --- Factura (CORREGIDO: Se asumió que el campo en el modelo Factura es 'fecha') ---

class FacturaSerializer(serializers.ModelSerializer):
    # Anidación para lectura (mostrar nombre del producto)
    producto_nombre = serializers.CharField(source='productoid.nombre', read_only=True)
    
    # Campo de escritura (para enviar solo el ID del producto)
    productoid = serializers.PrimaryKeyRelatedField(queryset=Productos.objects.all(), write_only=True)

    class Meta:
        model = Factura
        # CORRECCIÓN AQUÍ: cambiamos 'fecha_factura' por 'fecha'
        fields = (
            'id', 'codigofactura', 'cantidad', 'precio', 
            'producto_nombre', 'productoid', 'pedidoid'
        )
        read_only_fields = ('id', 'codigofactura', 'producto_nombre')