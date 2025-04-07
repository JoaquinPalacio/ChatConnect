from sqlmodel import SQLModel, create_engine
import os

DATABASE_URL = (
    f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@"
    f"{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
)

try:
    engine = create_engine(DATABASE_URL)
    SQLModel.metadata.create_all(engine)
    print("Base de datos conectada correctamente")
except Exception as e:
    print(f"Error al conectar la base de datos: {e}")
