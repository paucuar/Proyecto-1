import psycopg
import json

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "weaver",
    "host": "localhost",
    "port": "5432"
}

def obtener_sensores_geojson():
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            query = """
                SELECT
                    id,
                    nombre,
                    bateria_ptc,
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
                    "properties":{
                        "id": id_sensor,
                        "nombre": nombre,
                        "bateria_ptc": bateria,
                        "activa": activa
                    }
                }
                features.append(feature)

            geojson_final = {
                "type": "FeatureCollection",
                "features": features
            }

            return geojson_final

if __name__ == "__main__":
    datos_espaciales = obtener_sensores_geojson()
    with open ("sensores.geojson", "w", encoding="utf-8") as f:
        json.dump(datos_espaciales, f, indent=4, ensure_ascii=False)
    print("Archivo 'sensores.geojson generado correctamente.")