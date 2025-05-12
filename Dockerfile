# Imagen base de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos necesarios
COPY requirements.txt .
COPY ingesta.py .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Ejecutar el script al iniciar el contenedor
CMD ["python", "ingesta.py"]