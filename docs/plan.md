# Plan y Roadmap de ChatConnect

## Cambios futuros / Ideas

- Persistir mensajes del chat general en la base de datos.
- Implementar modelo de salas y mensajes por sala.
- Implementar modelo de amistad y sistema de solicitudes.
- Agregar mensajes privados entre usuarios.
- Historial de conversaciones con filtros (por usuario, sala, fecha, etc).

## Pendientes técnicos (Tech Debt)

- Agregar pruebas unitarias y de integración.
- Manejar errores y validaciones de forma más robusta en el frontend y backend.

## Análisis de decisiones

- Se eligió FastAPI por su rendimiento y facilidad para WebSockets.
- SQLModel se usa para aprovechar tipado y compatibilidad con SQLAlchemy.
- El manejo de usuarios y sesiones se realiza con cookies simples para facilitar el desarrollo inicial.
- Se optó por una arquitectura modular (rutas, modelos, utilidades) para facilitar futuras expansiones.

## Posibles problemas o mejoras

- Escalabilidad del chat en tiempo real si crece el número de usuarios.
- Seguridad en el manejo de sesiones y mensajes privados.
- Optimización de consultas para historial y búsqueda de mensajes.
- Mejorar la experiencia de usuario en dispositivos móviles.