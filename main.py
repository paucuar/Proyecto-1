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