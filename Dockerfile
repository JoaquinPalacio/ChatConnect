# 1. Partimos de una imagen ligera de Python 3.11
FROM python:3.11-slim

# 2. Definimos el directorio de trabajo
WORKDIR /app

# 3. Copiamos únicamente el archivo de dependencias y lo instalamos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Creamos un usuario no root para ejecutar la aplicación
RUN useradd -m dev
USER dev

# 5. Copiamos el resto del código de la aplicación
COPY . .

# 6. Exponemos el puerto 8000 para Uvicorn
EXPOSE 8000

# 7. Ejecutamos Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]