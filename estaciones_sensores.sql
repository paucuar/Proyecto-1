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

ALTER TABLE estaciones_sensores
ADD COLUMN IF NOT EXISTS geom GEOMETRY(Point, 4326);

UPDATE estaciones_sensores
SET geom = ST_SetSRID(ST_MakePoint(longitud, latitud), 4326);

CREATE INDEX IF NOT EXISTS idx_estaciones_geom
ON estaciones_sensores USING GIST (geom);

SELECT nombre, ST_AsText(geom) AS geometria_texto
FROM estaciones_sensores;

SELECT
    nombre,
    bateria_ptc,
    ROUND(
        ST_Distance(
            geom::geography,
            ST_SetSRID(ST_MakePoint(-0.376300, 39.469900), 4326)::geography
        )::numeric, 2
    ) AS distancia_metros
FROM estaciones_sensores
ORDER BY distancia_metros ASC;

TRUNCATE TABLE estaciones_sensores RESTART IDENTITY;
INSERT INTO estaciones_sensores (nombre, latitud, longitud, bateria_ptc, activa) VALUES
('Sensor Norte - València', 39.479100, -0.376200, 85, TRUE),
('Sensor Puerto', 39.460200, -0.332500, 15, TRUE),
('Sensor Albufera', 39.333300, -0.333300, 42, FALSE),
('Sensor Sierra Calderona', 39.702000, -0.456000, 95, TRUE);
UPDATE estaciones_sensores 
SET geom = ST_SetSRID(ST_MakePoint(longitud, latitud), 4326);

-- CONSULTAS ESPACIALES AVANZADAS
SELECT
    nombre,
    bateria_ptc,
    ROUND(
        ST_Distance(
            geom::geography,
            ST_SetSRID(ST_MakePoint(-0.376300, 39.469900), 4326)::geography
        )::numeric, 0
    ) AS distancia_m
FROM estaciones_sensores
WHERE ST_DWithin(
    geom::geography,
    ST_SetSRID(ST_MakePoint(-0.376300, 39.469900), 4326)::geography,
    20000
)
ORDER BY distancia_m ASC;

-- TABLA DE POLÍGONOS
 CREATE TABLE IF NOT EXISTS zonas_interes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    nivel_proteccion VARCHAR(50) DEFAULT 'Medio',
    geom GEOMETRY(Polygon, 4326)
);

INSERT INTO zonas_interes (nombre, nivel_proteccion, geom) VALUES
('Parque Natural de la Albufera', 'Alto',
ST_SetSRID(
    ST_GeomFromText('POLYGON((-0.3800 39.3800, -0.3000 39.3800, -0.3000 39.3000, -0.3800 39.3000, -0.3800 39.3800))'),
    4326
)
);

CREATE INDEX IF NOT EXISTS idx_zonas_geom ON zonas_interes USING GIST(geom);

SELECT
    e.nombre AS sensor,
    e.bateria_ptc,
    z.nombre AS zona_protegida,
    z.nivel_proteccion
FROM estaciones_sensores e
JOIN zonas_interes z
  ON ST_Contains(z.geom, e.geom);