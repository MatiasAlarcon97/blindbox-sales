# -------------------------------
# Dockerfile para el microservicio Blindbox Sales
# -------------------------------

# Imagen base ligera de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos de la aplicación
COPY app/ ./app
COPY app/requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto donde correrá Flask
EXPOSE 5000

# Comando por defecto para ejecutar la aplicación
CMD ["python", "app/app.py"]
