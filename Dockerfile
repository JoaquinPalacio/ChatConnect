# 1. Partimos de una imagen ligera de Python 3.11
FROM python:3.11-slim

# 2. Definimos el directorio de trabajo
WORKDIR /app

# 3. Copiamos únicamente el archivo de dependencias y lo instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copiamos el resto del código de la aplicación
COPY . .

# 5. Exponemos el puerto 8000 para Uvicorn
EXPOSE 8000

# 6. Ejecutamos Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]