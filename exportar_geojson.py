import os
import json
import psycopg
from dotenv import load_dotenv

# 1. Cargar las variables secretas del archivo .env
load_dotenv()

# 2. Configurar la conexión leyendo de las variables de entorno
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432))
}

def obtener_sensores_geojson():
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            query = """
                SELECT 
                    id, 
                    nombre, 
                    bateria_pct, 
                    activa,
                    ST_AsGeoJSON(geom) AS geometria_geojson
                FROM estaciones_sensores;
            """
            cur.execute(query)
            filas = cur.fetchall()

            features = []
            for fila in filas:
                id_sensor, nombre, bateria, activa, geom_json_str = fila
                feature = {
                    "type": "Feature",
                    "geometry": json.loads(geom_json_str),
                    "properties": {
                        "id": id_sensor,
                        "nombre": nombre,
                        "bateria_pct": bateria,
                        "activa": activa
                    }
                }
                features.append(feature)

            return {
                "type": "FeatureCollection",
                "features": features
            }

if __name__ == "__main__":
    datos_espaciales = obtener_sensores_geojson()
    
    with open("sensores.geojson", "w", encoding="utf-8") as f:
        json.dump(datos_espaciales, f, indent=4, ensure_ascii=False)
        
    print("Se ha generado el archivo de forma correcta")