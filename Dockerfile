# 1. Imagen de Python ligera (Linux Alpine/Slim)
FROM python:3.12-slim

# 2. Directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Archivo de requerimientos e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiar el código de nuestra API dentro del contenedor
COPY main.py .
COPY .env.example .

# 5. Exponer el puerto 8000 hacia el exterior
EXPOSE 8000

# 6. Comando para arrancar el servidor web al iniciar el contenedor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]