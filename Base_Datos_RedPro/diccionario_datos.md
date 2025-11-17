# Diccionario de Datos – Base de Datos RedPro

## Tabla: Categoria
| Campo           | Tipo      | Longitud | Nulo | Predeterminado | Descripción                           |
|-----------------|-----------|----------|------|-----------------|----------------------------------------|
| Id              | INT       | -        | NO   | IDENTITY(1,1)   | Identificador único de la categoría    |
| NombreCategoria | NVARCHAR  | 100      | NO   | -               | Nombre de la categoría                 |

---

## Tabla: Usuario
| Campo            | Tipo      | Longitud | Nulo | Predeterminado | Descripción                     |
|------------------|-----------|----------|------|-----------------|----------------------------------|
| Id               | INT       | -        | NO   | IDENTITY(1,1)   | Identificador único              |
| NombreUsuario    | NVARCHAR  | 100      | NO   | -               | Nombre de usuario único          |
| CorreoElectronico| NVARCHAR  | 100      | NO   | -               | Correo del usuario               |
| Contrasena       | NVARCHAR  | 100      | NO   | -               | Contraseña                       |
| FechaRegistro    | DATETIME  | -        | NO   | GETDATE()       | Fecha de registro                |
| Estado           | NVARCHAR  | 50       | NO   | -               | Estado del usuario               |

---

## Tabla: Clientes
| Campo      | Tipo      | Longitud | Nulo | Predeterminado | Descripción                      |
|------------|-----------|----------|------|-----------------|-----------------------------------|
| Id         | INT       | -        | NO   | IDENTITY(1,1)   | Identificador único               |
| NumeroRuc  | NVARCHAR  | 50       | NO   | -               | RUC único del cliente             |
| Nombre     | NVARCHAR  | 100      | NO   | -               | Nombre del cliente                |
| Apellido   | NVARCHAR  | 100      | NO   | -               | Apellido del cliente              |
| Telefono   | NVARCHAR  | 20       | NO   | -               | Teléfono único del cliente        |
| UsuarioId  | INT       | -        | SI   | -               | Relación opcional con Usuario     |

---

## Tabla: Proveedor
| Campo     | Tipo      | Longitud | Nulo | Predeterminado | Descripción                  |
|-----------|-----------|----------|------|-----------------|-------------------------------|
| Id        | INT       | -        | NO   | IDENTITY(1,1)   | Identificador único           |
| NIT       | NVARCHAR  | 50       | NO   | -               | NIT único                     |
| Nombre    | NVARCHAR  | 100      | NO   | -               | Nombre del proveedor          |
| Actividad | NVARCHAR  | 100      | SI   | -               | Actividad económica           |
| Pais      | NVARCHAR  | 50       | SI   | -               | País                          |
| Ciudad    | NVARCHAR  | 50       | SI   | -               | Ciudad                        |
| Direccion | NVARCHAR  | 200      | SI   | -               | Dirección                     |
| Telefono  | NVARCHAR  | 20       | SI   | -               | Teléfono único                |
| UsuarioId | INT       | -        | SI   | -               | Relación opcional con Usuario |

---

## Tabla: Establecimientos
| Campo               | Tipo      | Longitud | Nulo | Predeterminado | Descripción                        |
|---------------------|-----------|----------|------|-----------------|-------------------------------------|
| Id                  | INT       | -        | NO   | IDENTITY(1,1)   | Identificador único                 |
| CodigoEstablecimiento| NVARCHAR | 50       | NO   | -               | Código único del establecimiento    |
| NombreEstablecimiento| NVARCHAR | 100      | NO   | -               | Nombre del establecimiento          |
| Pais                | NVARCHAR  | 50       | SI   | -               | País                                |
| Ciudad              | NVARCHAR  | 50       | SI   | -               | Ciudad                              |
| Direccion           | NVARCHAR  | 200      | SI   | -               | Dirección                           |
| UsuarioId           | INT       | -        | SI   | -               | Referencia opcional a Usuario       |
| Tipo                | NVARCHAR  | 50       | SI   | -               | Tipo de establecimiento             |

---

## Tabla: EstadoProducto
| Campo         | Tipo      | Longitud | Nulo | Predeterminado | Descripción                   |
|---------------|-----------|----------|------|-----------------|-------------------------------|
| Id            | INT       | -        | NO   | IDENTITY(1,1)   | Identificador del estado      |
| EstadoProducto| NVARCHAR  | 100      | NO   | -               | Descripción del estado        |

---

## Tabla: EstadoPedido
| Campo       | Tipo      | Longitud | Nulo | Predeterminado | Descripción                   |
|-------------|-----------|----------|------|-----------------|-------------------------------|
| Id          | INT       | -        | NO   | IDENTITY(1,1)   | Identificador del estado      |
| EstadoPedido| NVARCHAR  | 100      | NO   | -               | Estado del pedido             |

---

## Tabla: MetodoPago
| Campo        | Tipo      | Longitud | Nulo | Predeterminado | Descripción                   |
|--------------|-----------|----------|------|-----------------|-------------------------------|
| Id           | INT       | -        | NO   | IDENTITY(1,1)   | Identificador                 |
| NombreMetodo | NVARCHAR  | 100      | NO   | -               | Nombre del método de pago     |

---

## Tabla: Productos
| Campo        | Tipo      | Longitud | Nulo | Predeterminado | Descripción                     |
|--------------|-----------|----------|------|-----------------|----------------------------------|
| Id           | INT       | -        | NO   | IDENTITY(1,1)   | Identificador único              |
| CodigoProducto| INT      | -        | NO   | -               | Código único del producto        |
| Nombre       | NVARCHAR  | 100      | NO   | -               | Nombre del producto              |
| Descripcion  | NVARCHAR  | 200      | SI   | -               | Descripción                      |
| Cantidad     | INT       | -        | NO   | 0               | Cantidad disponible              |
| Imagen       | NVARCHAR  | 200      | SI   | -               | Ruta de la imagen                |
| Precio       | DECIMAL   | 10,2     | NO   | -               | Precio del producto              |
| FechaCreacion| DATETIME  | -        | NO   | GETDATE()       | Fecha de creación                |
| ProveedorId  | INT       | -        | SI   | -               | Relación con proveedor           |
| EstadoId     | INT       | -        | SI   | -               | Relación con estado del producto |
| CategoriaId  | INT       | -        | SI   | -               | Relación con categoría           |

---

## Tabla: Pedido
| Campo          | Tipo      | Longitud | Nulo | Predeterminado | Descripción                      |
|----------------|-----------|----------|------|-----------------|-----------------------------------|
| Id             | INT       | -        | NO   | IDENTITY(1,1)   | Identificador único                |
| CodigoPedido   | INT       | -        | NO   | -               | Código único                      |
| Total          | DECIMAL   | 10,2     | NO   | -               | Total del pedido                   |
| FechaPedido    | DATETIME  | -        | NO   | GETDATE()       | Fecha del pedido                   |
| ClienteId      | INT       | -        | NO   | -               | Relación con cliente               |
| EstadoPedidoId | INT       | -        | SI   | -               | Estado del pedido                  |
| MetodoPagoId   | INT       | -        | SI   | -               | Método de pago                     |

---

## Tabla: Factura
| Campo         | Tipo      | Longitud | Nulo | Predeterminado | Descripción                |
|---------------|-----------|----------|------|-----------------|----------------------------|
| Id            | INT       | -        | NO   | IDENTITY(1,1)   | Identificador único        |
| CodigoFactura | INT       | -        | NO   | -               | Código único               |
| Cantidad      | INT       | -        | NO   | -               | Cantidad de productos      |
| Precio        | DECIMAL   | 10,2     | NO   | -               | Precio unitario            |
| PedidoId      | INT       | -        | NO   | -               | Referencia al pedido       |
| ProductoId    | INT       | -        | NO   | -               | Referencia al producto     |



### Relaciones

# **Claves foráneas**  
Clientes.UsuarioId → Usuario.Id (SET NULL)  
Proveedor.UsuarioId → Usuario.Id (SET NULL)  
Establecimientos.UsuarioId → Usuario.Id (SET NULL)  
Productos.ProveedorId → Proveedor.Id (SET NULL)  
Productos.EstadoId → EstadoProducto.Id (SET NULL)  
Productos.CategoriaId → Categoria.Id (SET NULL)  
Pedido.ClienteId → Clientes.Id (CASCADE)  
Pedido.EstadoPedidoId → EstadoPedido.Id (SET NULL)  
Pedido.MetodoPagoId → MetodoPago.Id (SET NULL)  
Factura.PedidoId → Pedido.Id (CASCADE)  
Factura.ProductoId → Productos.Id (CASCADE)

# **Restricciones UNIQUE**  
Usuario.NombreUsuario  
Clientes.NumeroRuc  
Clientes.Telefono  
Proveedor.NIT  
Proveedor.Telefono  
Establecimientos.CodigoEstablecimiento  
Productos.CodigoProducto  
Pedido.CodigoPedido  
Factura.CodigoFactura
