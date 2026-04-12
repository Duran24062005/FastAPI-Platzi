# Runtime Architecture

## Objetivo

Mantener el runtime organizado por capas para que cada cambio tenga una ubicación clara y no vuelva a mezclarse lógica HTTP, reglas de negocio y persistencia.

## Flujo de una request

`request -> router -> controller -> service -> repository -> database`

## Responsabilidad por carpeta

- `app/router/`: define rutas, parámetros, response models y dependencias FastAPI.
- `app/controller/`: traduce entre HTTP y la capa de aplicación. Aquí se convierten errores de negocio en respuestas HTTP coherentes.
- `app/service/`: contiene reglas de negocio y orquestación del dominio.
- `app/repository/`: encapsula acceso a SQLAlchemy y operaciones de persistencia.
- `app/schemas/`: contratos Pydantic para request/response y filtros.
- `app/core/`: piezas transversales del runtime, como excepciones de aplicación y constantes compartidas.
- `app/core/security/`: utilidades de autenticación y autorización, como JWT y bearer guards.
- `app/dependencies/`: composición de dependencias y factories para controllers, sesión DB y autenticación.
- `app/model/`: entidades ORM.
- `app/config/`: configuración e infraestructura base, especialmente base de datos.
- `app/middlewares/`: middlewares y guardas transversales.

## Reglas de implementación

- un router no hace queries ni crea sesiones
- un service no retorna `JSONResponse`
- un repository no conoce FastAPI
- un schema no vive dentro de router
- `core` no debe convertirse en un cajón genérico para cualquier cosa

## Convención para nuevos dominios

Cuando se agregue un nuevo dominio:

1. crear sus schemas en `app/schemas/`
2. crear su repository en `app/repository/`
3. crear su service en `app/service/`
4. crear su controller en `app/controller/`
5. exponer solo las rutas necesarias desde `app/router/`
6. registrar el wiring en `app/dependencies/`

## Auth y usuarios

- el registro publico y el login se resuelven desde `auth` usando un controller y un service dedicados
- el manejo JWT vive en `app/core/security/jwt.py`
- el bearer guard vive en `app/core/security/bearer.py`
- la existencia del usuario autenticado se verifica antes de permitir el acceso a rutas protegidas
- la autorizacion admin se resuelve desde `app/dependencies/` consultando el usuario actual en DB
- la gestion administrativa de usuarios vive bajo rutas `/api/v1/admin/users`
- la entidad `User` persiste un campo `role` y el runtime soporta `user` y `admin`
- `Base.metadata.create_all()` no migra la tabla `users`; si la base ya existe hay que agregar `role` manualmente o recrear la tabla
