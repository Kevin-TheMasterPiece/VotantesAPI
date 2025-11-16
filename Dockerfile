# Imagen base con Python
FROM python:3.11-slim

# Evita que Python guarde archivos .pyc y buffers
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crea y establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala dependencias del sistema necesarias para psycopg2 y otras librerías
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    apt-get clean

# Copia los archivos de dependencias e instálalas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo el código del proyecto
COPY . .

# Comando por defecto (se puede sobrescribir desde docker-compose)
CMD ["gunicorn", "VotantesAPI.wsgi:application", "--bind", "0.0.0.0:8000"]
