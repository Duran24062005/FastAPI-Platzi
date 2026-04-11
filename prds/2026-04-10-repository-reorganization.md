# Repository Reorganization PRD

## Problema y objetivo

El repositorio mezclaba runtime activo, ejemplos del curso, seeds, documentación y archivos de infraestructura en la raíz. Eso hacía menos clara la frontera entre lo que ejecuta la aplicación y lo que solo sirve como referencia o soporte.

El objetivo es reorganizar la estructura para que el runtime principal quede agrupado en un solo paquete, y el resto del material quede separado por responsabilidad.

## Scope

- crear `app/` para el runtime principal
- crear `docs/` para documentación técnica
- crear `prds/` para decisiones y planeación
- mantener `example/` separado del runtime
- actualizar imports y entrypoints para reflejar la nueva estructura

## Implementación

- mover el código operativo a `app/`
- convertir imports del runtime a rutas absolutas bajo `app`
- actualizar el entrypoint de Vercel y la referencia del contenedor
- documentar el criterio de organización

## Actores afectados

- desarrolladores que mantienen la API
- cualquier despliegue local, Docker o Vercel

## Impacto en contratos e integraciones

- cambia la ruta del entrypoint Python para Vercel
- cambia la referencia del módulo ASGI para ejecución con Uvicorn
- no cambian las rutas HTTP ni el contrato de la API

## Riesgos y validaciones

- riesgo de imports rotos después del movimiento
- riesgo de desalineación con configuración de despliegue

Validaciones aplicadas:

- recompilación de módulos Python
- revisión de referencias a rutas e imports clave
