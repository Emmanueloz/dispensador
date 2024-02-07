-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS dispensadorBD;

-- Crear la tabla Sensores
CREATE TABLE IF NOT EXISTS Sensores (
    idSensor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255),
    uso VARCHAR(255)
);

-- Crear la tabla Registros
CREATE TABLE IF NOT EXISTS Registros (
    idRegistro INT AUTO_INCREMENT PRIMARY KEY,
    estado VARCHAR(255),
    fecha DATE,
    hora TIME
);
