# Auth Register + Admin User Management

## Problema y objetivo

El runtime actual mezcla gestion de usuarios dentro del router `user` y no tiene un modelo real de autorizacion por rol. El objetivo de este cambio es:

- exponer un registro publico bajo `auth`
- separar la administracion de usuarios en rutas de admin
- introducir autorizacion real por rol persistido en base de datos

## Alcance implementado

- nuevo endpoint publico `POST /api/v1/auth/register`
- `POST /api/v1/auth/login` se mantiene como endpoint canonico de autenticacion
- eliminacion del endpoint legado `/api/v1/user/create_user/`
- nuevas rutas administrativas bajo `/api/v1/admin/users`
  - `GET /`
  - `GET /{id}`
  - `PUT /{id}`
  - `DELETE /{id}`

## Modelo y reglas

- la tabla `users` ahora incluye el campo `role`
- roles soportados en esta version:
  - `user`
  - `admin`
- `register` siempre crea usuarios con `role=user`
- los endpoints administrativos requieren un usuario autenticado con `role=admin`
- el acceso admin se valida contra el usuario actual en base de datos, no solo con el contenido del JWT

## Impacto en contratos e integraciones

- clientes que usaban `/api/v1/user/create_user/` deben migrar a `/api/v1/auth/register`
- `UserResponse` ahora expone `role`
- `AdminUserUpdate` requiere `email`, `password` y `role`
- el JWT ahora incluye `email` y `role`, aunque la autorizacion admin se sigue resolviendo con el estado actual en DB

## Persistencia y compatibilidad

- `Base.metadata.create_all()` no migra tablas existentes
- en bases ya creadas, la tabla `users` debe recrearse o alterarse manualmente para agregar la columna `role`
- los tests recrean el esquema completo en cada corrida, por eso no requieren una migracion adicional

## Riesgos y consideraciones

- esta iteracion mantiene passwords en texto plano, consistente con el runtime actual
- no se agrega expiracion de JWT en esta version
- si un usuario cambia de rol, la autorizacion efectiva la define la DB y no el token ya emitido
