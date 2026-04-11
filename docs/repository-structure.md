# Repository Structure

## Objetivo

Separar claramente el runtime principal de la aplicación de los materiales de ejemplo, la documentación y los archivos de infraestructura.

## Estructura

- `app/`: código fuente que participa directamente en la ejecución de la aplicación.
- `example/`: variantes didácticas, seeds y artefactos que no hacen parte del runtime principal.
- `docs/`: documentación técnica de mantenimiento y contexto operativo.
- `prds/`: documentos de planeación y decisiones de cambios relevantes.
- raíz del repositorio: archivos de infraestructura, dependencias, configuración de despliegue y datos locales.

## Criterio para `app/`

En `app/` vive únicamente el código necesario para:

- inicializar la API
- exponer endpoints
- aplicar middlewares
- definir modelos y acceso a datos
- resolver autenticación y lógica de servicio
- proveer entrypoints de ejecución o despliegue

## Fuera de `app/`

Se dejan fuera:

- documentación
- ejemplos y ejercicios del curso
- archivos de infraestructura como `Dockerfile`, `docker-compose.yml`, `vercel.json`
- dependencias como `requirements.txt`
- datos locales como `database.sqlite`
