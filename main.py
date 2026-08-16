import os
import json
import psycopg
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

load_dotenv()

app= FastAPI(
    title="API Geoespacial de Monitoreo Ambiental",
    description="Servicio backend para consulta de sensores y zonas protegidas con PostGIS",
    version="1.0.0"
)

def obtener_conexion_db():
    try:
        return psycopg.connect(
            dbname=os.getenv("DB_NAME", "postgres"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", 5432))
            )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al conectar con la base de datos: {str(e)}")

#Rutas de la API (ENDPOINTS)

@app.get("/")
def ruta_raiz():
    return{
        "mensaje": "Servidor Activo",
        "documentacion": "/docs"
    }
@app.get("/api/sensores")
def listar_sensores_geojson():
    with obtener_conexion_db() as conn:
        with conn.cursor() as cur:
            query = """
                SELECT
                    id,
                    nombre,
                    bateria_ptc,
                    activa,
                    ST_AsGeoJson(geom) AS geom_json
                    FROM estaciones_sensores;
                """
            cur.execute(query)
            filas = cur.fetchall()

            features = []
            for fila in filas:
                id_s, nombre, bateria, activa, geom_str = fila
                features.append({
                    "type": "Feature",
                    "geometry": json.loads(geom_str),
                    "properties":{
                        "id": id_s,
                        "nombre": nombre,
                        "bateria_ptc": bateria,
                        "activa": activa
                    }                
                })

            return{
                "type": "FeatureCollection",
                "features": features
            }

from fastapi import Query

@app.get("/api/sensores/alerta-bateria")
def sensores_alerta_bateria(umbral: int = Query(50, ge=0, le=100, description="Nivel máximo de batería para alertar")):
    try:
        with obtener_conexion_db() as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT 
                        id, 
                        nombre, 
                        bateria_ptc, 
                        activa, 
                        ST_AsGeoJSON(geom) AS geom_json
                    FROM estaciones_sensores
                    WHERE bateria_ptc <= %s
                    ORDER BY bateria_ptc ASC;
                """
                cur.execute(query, (int(umbral),))
                filas = cur.fetchall()

                features = []
                for fila in filas:
                    id_s, nombre, bateria, activa, geom_str = fila
                    
                    geometria_dict = json.loads(geom_str) if geom_str else None

                    features.append({
                        "type": "Feature",
                        "geometry": geometria_dict,
                        "properties": {
                            "id": id_s,
                            "nombre": nombre,
                            "bateria_ptc": bateria,
                            "activa": activa
                        }
                    })

                return {
                    "type": "FeatureCollection", 
                    "total_alertas": len(features), 
                    "features": features
                }
    except Exception as e:
        print(f"Error en alerta bateria: {e}")
        raise HTTPException(status_code=500, detail=f"Error en consulta de batería: {str(e)}")



@app.get("/api/sensores/cercanos")
def sensores_cercanos(
    lat: float = Query(..., description="Latitud del punto central"),
    lon: float = Query(..., description="Longitud del punto central"),
    radio_km: float = Query(20.0, description="Radio de búsqueda en kilómetros")
):
    with obtener_conexion_db() as conn:
        with conn.cursor() as cur:
            radio_metros = radio_km * 1000.0
            
            
            query = """
                SELECT 
                    id, 
                    nombre, 
                    bateria_ptc,
                    activa,
                    ROUND(ST_Distance(geom::geography, ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography)::numeric, 0) AS distancia_m,
                    ST_AsGeoJSON(geom) AS geom_json
                FROM estaciones_sensores
                WHERE ST_DWithin(
                    geom::geography,
                    ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography,
                    %s
                )
                ORDER BY distancia_m ASC;
            """
            cur.execute(query, (lon, lat, lon, lat, radio_metros))
            filas = cur.fetchall()

            features = []
            for fila in filas:
                id_s, nombre, bateria, activa, dist, geom_str = fila
                features.append({
                    "type": "Feature",
                    "geometry": json.loads(geom_str),
                    "properties": {
                        "id": id_s,
                        "nombre": nombre,
                        "bateria_ptc":bateria,
                        "activa": activa,
                        "distancia_metros": dist
                    }
                })

            return {
                "type": "FeatureCollection", 
                "total_encontrados": len(features), 
                "features": features
            }