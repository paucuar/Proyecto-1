CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS estaciones_sensores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(120) NOT NULL,
    bateria_ptc INT CHECK (bateria_ptc BETWEEN 0 AND 100),
    activa BOOLEAN DEFAULT TRUE,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    geom GEOMETRY(Point, 4326) NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_sensores_geom ON estaciones_sensores USING GIST (geom);

-- 4. Inserción de datos de prueba en Valencia (EPSG:4326 -> Longitud, Latitud)
INSERT INTO estaciones_sensores (nombre, bateria_ptc, activa, geom) VALUES
('Sensor Norte - València', 85, TRUE, ST_SetSRID(ST_MakePoint(-0.376200, 39.479100), 4326)),
('Sensor Puerto', 15, TRUE, ST_SetSRID(ST_MakePoint(-0.332500, 39.460200), 4326)),
('Sensor Albufera', 42, FALSE, ST_SetSRID(ST_MakePoint(-0.333300, 39.333300), 4326)),
('Sensor Sierra Calderona', 95, TRUE, ST_SetSRID(ST_MakePoint(-0.456000, 39.702000), 4326))
ON CONFLICT DO NOTHING;