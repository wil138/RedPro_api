-- =====================================================
-- Base de datos: RedPro
create database RedPro

use RedPro


-- Tabla Categoria
-- ================================
create table Categoria (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    NombreCategoria NVARCHAR(100) NOT NULL
);

-- ================================
-- Tabla Usuario
-- ================================
CREATE TABLE Usuario (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    NombreUsuario NVARCHAR(100) UNIQUE NOT NULL,
    CorreoElectronico NVARCHAR(100) NOT NULL,
    Contrasena NVARCHAR(100) NOT NULL,
    FechaRegistro DATETIME NOT NULL DEFAULT GETDATE(),
    Estado NVARCHAR(50) NOT NULL
);

-- ================================
-- Tabla Clientes
-- ================================
CREATE TABLE Clientes (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    NumeroRuc NVARCHAR(50) UNIQUE NOT NULL,
    Nombre NVARCHAR(100) NOT NULL,
    Apellido NVARCHAR(100) NOT NULL,
    Telefono NVARCHAR(20) UNIQUE NOT NULL,
    UsuarioId INT NULL,
    CONSTRAINT FK_Clientes_Usuario FOREIGN KEY (UsuarioId)
        REFERENCES Usuario(Id)
        ON DELETE SET NULL
);

-- ================================
-- Tabla Proveedor
-- ================================
CREATE TABLE Proveedor (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    NIT NVARCHAR(50) UNIQUE NOT NULL,
    Nombre NVARCHAR(100) NOT NULL,
    Actividad NVARCHAR(100),
    Pais NVARCHAR(50),
    Ciudad NVARCHAR(50),
    Direccion NVARCHAR(200),
    Telefono NVARCHAR(20) UNIQUE,
    UsuarioId INT NULL,
    CONSTRAINT FK_Proveedor_Usuario FOREIGN KEY (UsuarioId)
        REFERENCES Usuario(Id)
        ON DELETE SET NULL
);

-- ================================
-- Tabla Establecimientos
-- ================================
CREATE TABLE Establecimientos (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    CodigoEstablecimiento NVARCHAR(50) UNIQUE NOT NULL,
    NombreEstablecimiento NVARCHAR(100) NOT NULL,
    Pais NVARCHAR(50),
    Ciudad NVARCHAR(50),
    Direccion NVARCHAR(200),
    UsuarioId INT NULL,
    Tipo NVARCHAR(50),
    CONSTRAINT FK_Establecimientos_Usuario FOREIGN KEY (UsuarioId)
        REFERENCES Usuario(Id)
        ON DELETE SET NULL
);

-- ================================
-- Tabla EstadoProducto
-- ================================
CREATE TABLE EstadoProducto (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    EstadoProducto NVARCHAR(100) NOT NULL
);

-- ================================
-- Tabla EstadoPedido
-- ================================
CREATE TABLE EstadoPedido (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    EstadoPedido NVARCHAR(100) NOT NULL
);

-- ================================
-- Tabla MetodoPago
-- ================================
CREATE TABLE MetodoPago (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    NombreMetodo NVARCHAR(100) NOT NULL
);

-- ================================
-- Tabla Productos
-- ================================
CREATE TABLE Productos (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    CodigoProducto INT UNIQUE NOT NULL,
    Nombre NVARCHAR(100) NOT NULL,
    Descripcion NVARCHAR(200),
    Cantidad INT NOT NULL DEFAULT 0,
    Imagen NVARCHAR(200),
    Precio DECIMAL(10,2) NOT NULL,
    FechaCreacion DATETIME NOT NULL DEFAULT GETDATE(),
    ProveedorId INT NULL,
    EstadoId INT NULL,
    CategoriaId INT NULL,
    CONSTRAINT FK_Productos_Proveedor FOREIGN KEY (ProveedorId)
        REFERENCES Proveedor(Id)
        ON DELETE SET NULL,
    CONSTRAINT FK_Productos_EstadoProducto FOREIGN KEY (EstadoId)
        REFERENCES EstadoProducto(Id)
        ON DELETE SET NULL,
    CONSTRAINT FK_Productos_Categoria FOREIGN KEY (CategoriaId)
        REFERENCES Categoria(Id)
        ON DELETE SET NULL
);

-- ================================
-- Tabla Pedido
-- ================================
CREATE TABLE Pedido (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    CodigoPedido INT UNIQUE NOT NULL,
    Total DECIMAL(10,2) NOT NULL,
    FechaPedido DATETIME NOT NULL DEFAULT GETDATE(),
    ClienteId INT NOT NULL,
    EstadoPedidoId INT NULL,         -- Cambiado a NULL
    MetodoPagoId INT NULL,           -- Cambiado a NULL
    CONSTRAINT FK_Pedido_Cliente FOREIGN KEY (ClienteId)
        REFERENCES Clientes(Id)
        ON DELETE CASCADE,
    CONSTRAINT FK_Pedido_EstadoPedido FOREIGN KEY (EstadoPedidoId)
        REFERENCES EstadoPedido(Id)
        ON DELETE SET NULL,
    CONSTRAINT FK_Pedido_MetodoPago FOREIGN KEY (MetodoPagoId)
        REFERENCES MetodoPago(Id)
        ON DELETE SET NULL
);

-- ================================
-- Tabla Factura
-- ================================
CREATE TABLE Factura (
    Id INT IDENTITY(1,1) PRIMARY KEY,
    CodigoFactura INT UNIQUE NOT NULL,
    Cantidad INT NOT NULL,
    Precio DECIMAL(10,2) NOT NULL,
    PedidoId INT NOT NULL,
    ProductoId INT NOT NULL,
    CONSTRAINT FK_Factura_Pedido FOREIGN KEY (PedidoId)
        REFERENCES Pedido(Id)
        ON DELETE CASCADE,
    CONSTRAINT FK_Factura_Producto FOREIGN KEY (ProductoId)
        REFERENCES Productos(Id)
        ON DELETE CASCADE
);