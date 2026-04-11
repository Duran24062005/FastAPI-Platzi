# PRD: Refactorización a Arquitectura por Capas con Repository y Core

## Problema actual

La aplicación tenía lógica HTTP, validación, acceso a base de datos y reglas de negocio mezcladas dentro de los routers. Eso generaba acoplamiento fuerte entre FastAPI, SQLAlchemy y la lógica funcional, dificultando mantenimiento, testing y extensión del proyecto.

También existían inconsistencias relevantes:

- los schemas Pydantic vivían dentro de los routers
- el login generaba JWT sin autenticar contra base de datos
- el guard `JWTBearer` estaba implementado con firma de middleware, no de dependency
- coexistían dos modelos de usuario (`User` y `User2`) sin una responsabilidad clara

## Objetivo

Reorganizar el runtime para dejar una arquitectura limpia y trazable basada en capas:

- `router`: solo definición de rutas y dependencias FastAPI
- `controller`: traducción entre capa HTTP y capa de aplicación
- `service`: lógica de negocio
- `repository`: acceso a persistencia
- `schemas`: contratos de entrada y salida
- `core`: piezas transversales, especialmente excepciones de aplicación

## Alcance

Incluido en esta refactorización:

- dominio `movies`
- dominio `users`
- flujo `auth` para login y validación JWT
- dependencia compartida de base de datos
- documentación de arquitectura y convenciones
- pruebas base con `TestClient`

No incluido:

- hashing de contraseñas
- migraciones formales de base de datos
- separación por bounded contexts o módulos independientes

## Decisiones de diseño

### Core

Se crea `app/core` como capa transversal del runtime. Su responsabilidad actual es centralizar excepciones de aplicación y constantes compartidas. No contiene lógica específica de dominio.

### Repository

Cada dominio usa un repository dedicado que encapsula acceso a SQLAlchemy y sesión inyectada. Los repositories no conocen FastAPI ni retornan respuestas HTTP.

### Controller

Los controllers reciben datos ya validados y traducen excepciones de aplicación a `HTTPException`. De esta forma, el mapeo HTTP queda fuera de service y de router.

### Usuario persistente

Se elimina la duplicidad conceptual entre `User` y `User2` y se deja un único modelo persistente `User` sobre la tabla `users`.

### Auth

El login ahora valida credenciales contra base de datos antes de emitir el token. `JWTBearer` se reescribe como dependencia válida de FastAPI y verifica que el usuario del token exista.

## Impacto técnico

- cambia la estructura interna del runtime en `app/`
- cambian imports y dependencias entre capas
- el endpoint de login mantiene su ruta `/Login`, pero ahora autentica realmente
- se introduce el endpoint `GET /movies/search` para filtrar por categoría sin volver a mezclar lógica en un router duplicado

## Riesgos y edge cases

- la tabla antigua `users2` puede seguir existiendo en bases previas, pero deja de ser usada por el runtime
- las contraseñas siguen en texto plano porque este cambio se enfocó en arquitectura, no en seguridad avanzada
- si existen consumidores que dependían del comportamiento incorrecto del login anterior, ahora recibirán errores de autenticación válidos

## Validaciones requeridas

- arranque correcto de la app
- importación correcta del runtime
- CRUD de películas funcionando por capas
- endpoints de usuarios protegidos por JWT
- login autenticando contra base de datos
- traducción consistente de errores funcionales a respuestas HTTP
