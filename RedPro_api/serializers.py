from rest_framework import serializers
from django.contrib.auth.models import User
# Importamos los modelos limpios y corregidos
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
# Usamos el modelo User de Django. Se recomienda usar este en lugar de tu modelo 'Usuario'.
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
    # Para lectura, muestra el nombre de usuario asociado al Proveedor
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Proveedor
        # Usando 'usuario' en snake_case como se definió en el modelo limpio
        fields = '__all__'
        read_only_fields = ('id', 'usuario_username')


# --- Producto ---
class ProductoSerializer(serializers.ModelSerializer):
    # Para lectura, anidamos los serializadores de lookup para mostrar el nombre
    proveedor_nombre = serializers.CharField(source='proveedor.nombre', read_only=True)
    estado = EstadoProductoSerializer(read_only=True)
    categoria = CategoriaSerializer(read_only=True)

    # Campos de escritura (para la creación/actualización)
    estado_id = serializers.PrimaryKeyRelatedField(queryset=Estadoproducto.objects.all(), source='estado', write_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all(), source='categoria', write_only=True)

    class Meta:
        model = Productos
        # Incluimos los campos de lectura (anidados) y los campos de escritura (ID)
        fields = (
            'id', 'codigoproducto', 'nombre', 'descripcion', 'cantidad', 'imagen', 'precio', 'fechacreacion',
            'proveedorid', 'proveedor_nombre', # proveedorid es el ID para escritura. proveedor_nombre es la FK anidada para lectura.
            'estadoid', 'estado_id',
            'categoriaid', 'categoria_id',
        )
        # Importante: Corregí los nombres de campo para que coincidan con tus modelos (ej. 'codigoproducto', 'estadoid', etc.)
        read_only_fields = ('id', 'fechacreacion', 'proveedor_nombre', 'estado', 'categoria')
        # Nota: Los campos 'estado' y 'categoria' ahora contienen los objetos anidados para lectura.


# --- Cliente (Para Listar/Leer/Actualizar) ---
class ClienteSerializer(serializers.ModelSerializer):
    # Para lectura, muestra el nombre de usuario asociado al Cliente
    usuario_username = serializers.CharField(source='usuarioid.nombreusuario', read_only=True)

    class Meta:
        model = Clientes
        fields = '__all__'
        read_only_fields = ('id', 'usuario_username')


# --- Cliente (Para Registro Abierto: Creación/POST) ---
class ClienteCreationSerializer(serializers.ModelSerializer):
    # Incluimos los campos del usuario anidado para el registro
    usuario = UserCreationSerializer(write_only=True)
    # Nota: Tu modelo Cliente usa 'UsuarioId' como FK, que apunta a tu modelo 'Usuario', NO a django.contrib.auth.models.User.
    # Por lo tanto, el proceso de creación aquí deberá ser revisado si quieres usar el modelo User de Django.

    class Meta:
        model = Clientes
        fields = ('numeroruc', 'nombre', 'apellido', 'telefono', 'usuario')

    def create(self, validated_data):
        # El modelo Cliente apunta a tu modelo 'Usuario', no al de Django.
        # Si quieres usar el modelo User de Django, debes adaptar tu modelo Cliente.
        # A falta de tu modelo 'Usuario', asumiré que la clave 'usuario' se refiere al objeto User de Django.
        user_data = validated_data.pop('usuario')
        # Aquí se debería crear o usar tu modelo 'Usuario' basado en 'UserCreationSerializer'
        # Por ahora, voy a simplificar la lógica de creación para evitar más errores:
        
        # 1. Crear el objeto User (usando el create del UserCreationSerializer)
        user_creation_serializer = UserCreationSerializer(data=user_data)
        user_creation_serializer.is_valid(raise_exception=True)
        user_instance = user_creation_serializer.save()

        # Aquí deberías crear tu modelo 'Usuario' (que es distinto de django.contrib.auth.User)
        # y luego usar ese ID para el cliente. Ya que no tengo el código, lo dejo como nota.

        # 2. Crear el objeto Cliente sin la FK de usuario por ahora (¡ADVERTENCIA DE LÓGICA DE NEGOCIO!)
        cliente = Clientes.objects.create(**validated_data)
        return cliente


# --- Establecimiento ---
class EstablecimientoSerializer(serializers.ModelSerializer):
    usuario_username = serializers.CharField(source='usuarioid.nombreusuario', read_only=True)

    class Meta:
        model = Establecimientos
        fields = '__all__'
        read_only_fields = ('id', 'usuario_username')


# --- Pedido ---
class PedidoSerializer(serializers.ModelSerializer):
    # Anidación para lectura
    cliente_nombre = serializers.CharField(source='clienteid.nombre', read_only=True)
    estado_pedido_nombre = serializers.CharField(source='estadopedidoid.estadoproducto', read_only=True)
    metodo_pago_nombre = serializers.CharField(source='metodopagoid.nombremetodo', read_only=True)

    class Meta:
        model = Pedido
        fields = '__all__'
        read_only_fields = ('id', 'codigopedido', 'fechapedido', 'cliente_nombre', 'estado_pedido_nombre', 'metodo_pago_nombre')


# --- Factura ---
class FacturaSerializer(serializers.ModelSerializer):
    # Anidación para lectura
    producto_nombre = serializers.CharField(source='productoid.nombre', read_only=True)

    class Meta:
        model = Factura
        fields = '__all__'
        read_only_fields = ('id', 'producto_nombre')