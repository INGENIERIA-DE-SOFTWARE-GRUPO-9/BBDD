CREATE DATABASE IF NOT EXISTS gestion_hotelera_1;
USE gestion_hotelera_1;

CREATE TABLE Usuarios (
    ID_Usuario INT AUTO_INCREMENT PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Correo_Electronico VARCHAR(100) UNIQUE NOT NULL,
    Telefono VARCHAR(15),
    Password_Hash VARCHAR(255) NOT NULL,  -- Contraseña encriptada
    Estado_Cuenta ENUM('Activo', 'Inactivo', 'Bloqueado') DEFAULT 'Activo',
    Tipo_Usuario ENUM('Cliente', 'Administrador') NOT NULL,  -- Diferenciación entre cliente y admin
    Direccion VARCHAR(255),  -- Solo para clientes
    Fecha_Nacimiento DATE,   -- Solo para clientes
    Metodo_Pago VARCHAR(50),  -- Solo para clientes
    Rol VARCHAR(50),  -- Solo para administradores
    Fecha_Contratacion DATE  -- Solo para administradores
);

CREATE TABLE Habitaciones (
    ID_Habitacion INT AUTO_INCREMENT PRIMARY KEY,
    Numero_Habitacion VARCHAR(10) UNIQUE NOT NULL,
    Tipo_Habitacion VARCHAR(50),
    Precio DECIMAL(10, 2) NOT NULL,
    Descripcion TEXT,  -- Descripción de la habitación
    Imagenes JSON,     -- URLs de imágenes de la habitación (almacenado en formato JSON)
    Estado ENUM('Disponible', 'Reservada', 'Ocupada') DEFAULT 'Disponible'
);

CREATE TABLE Reservas (
    ID_Reserva INT AUTO_INCREMENT PRIMARY KEY,
    ID_Usuario INT,  -- Relacionado con el cliente (Usuario)
    ID_Habitacion INT,  -- Relacionado con la habitación
    Fecha_Reserva DATE NOT NULL,
    Fecha_Checkin DATE NOT NULL,
    Fecha_Checkout DATE NOT NULL,
    Numero_Huespedes INT DEFAULT 1,  -- Número de personas
    Estado_Reserva ENUM('Confirmada', 'Cancelada', 'Pendiente') DEFAULT 'Pendiente',
    Metodo_Pago VARCHAR(50),
    Notas_Especiales TEXT,  -- Notas adicionales solicitadas por el cliente
    FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID_Usuario),  -- Relacion con Usuarios
    FOREIGN KEY (ID_Habitacion) REFERENCES Habitaciones(ID_Habitacion)  -- Relacion con Habitaciones
);

CREATE TABLE Pagos (
    ID_Pago INT AUTO_INCREMENT PRIMARY KEY,
    ID_Reserva INT,  -- Relacionado con la reserva
    ID_SistemaPago INT,  -- Relacionado con el sistema de pago
    Monto DECIMAL(10, 2) NOT NULL,
    Fecha_Pago DATE NOT NULL,
    Estado_Pago ENUM('Completado', 'Fallido', 'Pendiente') DEFAULT 'Pendiente',
    Moneda VARCHAR(10) DEFAULT 'USD',  -- Moneda utilizada en el pago
    ID_Transaccion VARCHAR(100),  -- ID de la transacción de pago
    FOREIGN KEY (ID_Reserva) REFERENCES Reservas(ID_Reserva),  -- Relacion con Reservas
    FOREIGN KEY (ID_SistemaPago) REFERENCES SistemaPago(ID_SistemaPago)  -- Relacion con Sistema de Pago
);

CREATE TABLE SistemaPago (
    ID_SistemaPago INT AUTO_INCREMENT PRIMARY KEY,
    NombreSistema VARCHAR(100) NOT NULL,  -- Nombre de la pasarela de pago (PayPal, Stripe, etc.)
    TipoTransaccion VARCHAR(50),  -- Tipo de transacción: Tarjeta de Crédito, Débito, PayPal, etc.
    URL VARCHAR(255)  -- URL de integración de la pasarela de pago
);

CREATE TABLE HistorialActividades (
    ID_Actividad INT AUTO_INCREMENT PRIMARY KEY,
    ID_Usuario INT,  -- Relacionado con el usuario que realiza la acción
    Tipo_Accion VARCHAR(100),  -- Tipo de acción realizada (ej. Crear reserva, Cancelar reserva)
    Descripcion TEXT,  -- Detalle de la actividad realizada
    Fecha_Hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Hora de la acción
    FOREIGN KEY (ID_Usuario) REFERENCES Usuarios(ID_Usuario)  -- Relacion con Usuarios
);