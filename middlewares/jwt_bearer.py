from fastapi import Request, HTTPException
from jwt_manager import decode_token
from fastapi.security import HTTPBearer
from config.database import Session
from model.movie_model import User2 

# class JWTBearer(HTTPBearer):
#     db = Session()
#     e = db.query(User2).filter(User2.email)
#     async def __call__(self, request: Request):
#         auth = await super().__call__(request)
#         data = decode_token(auth.credentials)
#         if data['email'] != 'alexi@gmail.com':
#             raise HTTPException(status_code=403, detail='the credential are invalid')


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request, call_next):
        auth = await super().__call__(request)
        data = decode_token(auth.credentials)

        # Iniciar sesión en la base de datos
        db = Session()

        try:
            # Consultar el usuario por su email
            user = db.query(User2).filter(User2.email == data['email']).first()

            # Si no se encuentra el usuario, lanzar un error 404
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # Si el email no coincide, lanzar un error 403
            if user.email != 'alexi@gmail.com':
                raise HTTPException(status_code=403, detail="The credentials are invalid")

        except Exception as e:
            # Capturar cualquier otro error inesperado y lanzar un error 500
            raise HTTPException(status_code=500, detail=str(e))
        
        finally:
            # Cerrar la sesión para evitar fugas de conexión
            db.close()

        # Continuar con la solicitud
        return await call_next(request)