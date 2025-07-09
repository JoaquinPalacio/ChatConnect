# Chat Connect

Aplicación web de chat en tiempo real construida con **FastAPI**, **WebSockets** y **PostgreSQL**. Permite a los usuarios registrarse, iniciar sesión y participar en un chat general en vivo.

## Demo

![Demo ChatConnect](docs/demo.gif)

## Características

- Registro e inicio de sesión de usuarios (con JWT y cookies).
- Chat general en tiempo real usando WebSockets.
- Interfaz moderna con Bootstrap.
- Dockerizado para fácil despliegue.

## Tecnologías utilizadas

- Python, FastAPI, SQLModel
- PostgreSQL
- Docker, Docker Compose
- WebSockets
- Bootstrap

## Requisitos previos

- [Docker](https://www.docker.com/) y [Docker Compose](https://docs.docker.com/compose/)
- (Opcional) Python 3.11+ para ejecución local sin Docker

## Instalación

### Con Docker (recomendado)

```bash
git clone https://github.com/joaquinpalacio/ChatConnect.git
cd ChatConnect
cp .env.example .env
docker-compose up --build
```
Asegurarse de tener Docker instalado.

### Instalación local (sin Docker)

```bash
git clone https://github.com/tuusuario/ChatConnect.git
cd ChatConnect
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn main:app --reload
```

## Variables de entorno

Las variables necesarias se definen en .env. Puedes usar el archivo .env.example como base:

```
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=chatconnect
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql://admin:admin@db:5432/chatconnect
SECRET_KEY=supersecretkey
```

## Uso

- Accede a la app: [http://localhost:8002](http://localhost:8002)
- Documentación de la API: [http://localhost:8002/docs](http://localhost:8002/docs)


## Estructura del proyecto

```text
ChatConnect/
├── main.py                # Punto de entrada de la app
├── db/                    # Conexión y utilidades de base de datos
├── routes/                # Rutas de la API (auth, chat)
├── templates/             # Plantillas HTML (Jinja2)
├── utils/                 # Utilidades (hash, seguridad, helpers)
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## Contribución

¡Las contribuciones son bienvenidas! Por favor, abre un issue o un pull request.

## Licencia

Este proyecto está bajo la licencia MIT.