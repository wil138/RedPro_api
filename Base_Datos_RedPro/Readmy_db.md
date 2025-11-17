# Base de Datos – RedPro

Este repositorio contiene el diseño estructurado y los scripts SQL de la base de datos del sistema **RedPro**, enfocado en la gestión integral de usuarios, clientes, proveedores, productos, pedidos y facturación.

---

## 📁 Estructura del Proyecto

````
diseñobdd_impulsonica/ 
├── creacion_db.sql # Script para crear todas las tablas 
├── diccionario_datos.md # Documento con descripción de todas las tablas
├── diagrama-logico.png # Imagen del diagrama lógico relacional 
````

---

## 🧩 Tecnologías Utilizadas

- **SQL Server (T-SQL)**
- Integración a backend (framework libre)
- Estructura normalizada con claves externas

---

## 📜 Tablas del Sistema (Resumen)

| Tabla / Entidad     | Descripción |
|---------------------|-------------|
| **Categoria**       | Clasificación asignada a productos. |
| **Usuario**         | Gestión de usuarios del sistema: credenciales, estado y registro. |
| **Clientes**        | Personas que realizan pedidos; pueden estar asociadas a un usuario. |
| **Proveedor**       | Empresas o personas que proveen productos. |
| **Establecimientos**| Sucursales o puntos de operación. |
| **EstadoProducto**  | Estados posibles de un producto (Disponible, Agotado, etc.). |
| **EstadoPedido**    | Estados posibles de un pedido. |
| **MetodoPago**      | Métodos de pago reconocidos por el sistema. |
| **Productos**       | Inventario: datos, precios, proveedores y estado. |
| **Pedido**          | Transacción principal realizada por un cliente. |
| **Factura**         | Línea de detalle asociada a un pedido y producto. |

---

## 📂 Scripts disponibles

### 🔹 `creacion_db.sql`
Crea las entidades principales del sistema con sus relaciones:

- Categorías
- Usuarios
- Clientes
- Proveedores
- Establecimientos
- Estados de productos
- Estados de pedidos
- Métodos de pago
- Productos
- Pedidos
- Facturas

Incluye reglas de integridad:  
`ON DELETE SET NULL` y `ON DELETE CASCADE` según la lógica de negocio.

---

## 🚀 Cómo usar esta base de datos

1. Abrí **SQL Server Management Studio**.  
2. Ejecutá `creacion_db.sql`.  
3. Verificá claves externas y relaciones generadas.  
4. Integra el modelo en tu backend (ORM, migraciones, etc.).  

---

## 📝 Recomendaciones

- Validar tipos de datos y relaciones antes del despliegue.
- Mantener actualizado `diccionario_datos.md` para documentación técnica.
- Controlar cambios mediante Git en cada actualización estructural.
- Revisar comportamiento de eliminaciones (SET NULL / CASCADE).

---
