CREATE DATABASE ListaTareas;

CREATE TABLE Usuarios (
    id INT IDENTITY(1,1) PRIMARY KEY,
    username NVARCHAR(50) NOT NULL UNIQUE,
    password NVARCHAR(255) NOT NULL
);
GO

-- Crear tabla de tareas
CREATE TABLE Tareas (
    id INT IDENTITY(1,1) PRIMARY KEY,
    usuario_id INT NOT NULL,
    descripcion NVARCHAR(255) NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id) ON DELETE CASCADE
);
GO

select * from Usuarios
select * from Tareas