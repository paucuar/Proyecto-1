# Spatial Sensor API (GeoJSON & PostGIS Microservice)

# Microservice developed in Python with **FastAPI** and a Spatial Database **PostgreSQL + PostGIS**. Packaged and Orchestrated by **Docker & Docker Compose**. Designed for ingest, spatial analytics querying, and IoT telemetry serialization in GeoJSON standard.

##System Architechture

```text
[Client/Frontend]
        |
        ▼ (HTTP/REST)
[Docker Container: FastAPI + Uvicorn] (Port: 8000)
        |
        ▼ (host.docker.internal Tunnel/ Isolated Network)
[PostgreSQL + PostGIS Extension] (Port 5432)