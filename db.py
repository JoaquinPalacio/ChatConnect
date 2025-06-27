from sqlmodel import SQLModel, create_engine
import os

DATABASE_URL = os.environ["DATABASE_URL"]
try:
    engine = create_engine(DATABASE_URL)
    SQLModel.metadata.create_all(engine)
    print("Base de datos conectada correctamente")
except Exception as e:
    print(f"Error al conectar la base de datos: {e}")
