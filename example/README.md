# Example

Este directorio agrupa archivos de ejemplo, ejercicios del curso y utilidades de seed que no forman parte del runtime principal de la aplicación.

El sistema activo usa `app/main.py` como app principal y `app/api/index.py` como entrypoint para despliegue.

Contenido movido:

- `main2.py`: versión didáctica inicial con almacenamiento en memoria.
- `main3.py`: versión intermedia del curso con mezcla de ejemplos y lógica antigua.
- `db.py`: dataset en memoria usado por los ejemplos.
- `migrate_to_postgres.py`: script de carga de datos de ejemplo.
- `services.py`: helpers para que los ejemplos queden autocontenidos.
