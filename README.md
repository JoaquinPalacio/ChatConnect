# Chat Connect

Aplicación web de chat en tiempo real construida con **FastAPI**, **WebSockets** y **PostgreSQL**. Permite a los usuarios registrarse, iniciar sesión y participar en salas públicas y privadas, además de un chat general.

## Demo

![Demo ChatConnect](docs/demo.gif)

## Características

- Registro e inicio de sesión de usuarios (con JWT y cookies).
- Chat general y salas personalizadas en tiempo real usando WebSockets.
- Salas públicas y privadas (con contraseña).
- Mensajes persistentes por sala.
- Interfaz moderna con Bootstrap.
- Dockerizado para fácil despliegue.
- Tests automatizados con Pytest.
- Arquitectura modular y escalable.

## Tecnologías utilizadas

- Python, FastAPI, SQLModel
- PostgreSQL
- Docker, Docker Compose
- WebSockets
- Bootstrap
- Pytest

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

## Funcionalidades principales

- **Registro e inicio de sesión:** Los usuarios pueden crear cuentas y autenticarse.
- **Chat general:** Todos los usuarios pueden participar en el chat global.
- **Salas personalizadas:** Crea salas públicas o privadas (con contraseña).
- **Mensajes persistentes:** Los mensajes se guardan por sala y usuario.
- **Interfaz responsiva:** Bootstrap para una experiencia moderna.
- **Gestión de sesiones:** Solo usuarios autenticados pueden crear salas o enviar mensajes.
- **Tests:** Pruebas unitarias para usuarios, salas y mensajes.

## Estructura del proyecto

```text
ChatConnect/
├── main.py                # Punto de entrada de la app
├── api/                   # Rutas y funcionalidades de la app
├── core/                  # Lógica central de la app
├── crud/                  # Funciones de acceso a datos para los modelos
├── models/                # Modelos de la base de datos
├── services/              # Lógica de negocio
├── db/                    # Configuración y conexión a la base de datos
├── templates/             # Plantillas HTML (Jinja2)
├── tests/                 # Tests de funcionamiento
├── docker-compose.yml
├── Dockerfile
├── .env.example
└── README.md
```

## Ejecutar tests

Para ejecutar los tests automáticos:

```bash
pytest
```

## Contribución

¡Las contribuciones son bienvenidas! Por favor, abre un issue o un pull request.

## Licencia

Este proyecto está bajo la licencia MIT.