-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS dispensadorBD;

CREATE TABLE tareas (
    idTarea INT PRIMARY KEY,
    idSensor INT,
    tipo VARCHAR(255),
    fechaRegistro DATE,
    horaRegistro TIME,
    tiempo INT,
    unidadtiempo VARCHAR(50)
);

-- Crear la tabla Registros
CREATE TABLE IF NOT EXISTS Registros (
    idRegistro INT AUTO_INCREMENT PRIMARY KEY,
    estado VARCHAR(255),
    fecha DATE,
    hora TIME
);
