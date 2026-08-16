CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS estaciones_sensores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    latitud NUMERIC(9,6) NOT NULL,
    longitud NUMERIC(9,6) NOT NULL,
    bateria_ptc INT CHECK (bateria_ptc BETWEEN 0 AND 100),
    activa BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO estaciones_sensores (nombre, latitud, longitud, bateria_ptc, activa) VALUES
('Sensor Norte - València', 39.479100, -0.376200, 85, TRUE),
('Sensor Puerto', 39.460200, -0.332500, 15, TRUE),
('Sensor Albufera', 39.333300, -0.333300, 42, FALSE),
('Sensor Sierra Calderona', 39.702000, -0.456000, 95, TRUE);