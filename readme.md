# Spatial Sensor API (GeoJSON & PostGIS Microservice)

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![PostGIS](https://img.shields.io/badge/PostGIS-Spatial%20DB-0064a5?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

# Microservice developed in Python with **FastAPI** and a Spatial Database **PostgreSQL + PostGIS**. Packaged and Orchestrated by **Docker & Docker Compose**. Designed for ingest, spatial analytics querying, and IoT telemetry serialization in GeoJSON standard.

## System Architechture

```text
[Client/Frontend]
        |
        ▼ (HTTP/REST)
[Docker Container: FastAPI + Uvicorn] (Port: 8000)
        |
        ▼ (host.docker.internal Tunnel/ Isolated Network)
[PostgreSQL + PostGIS Extension] (Port 5432)