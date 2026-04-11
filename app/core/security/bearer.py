from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config.database import SessionLocal
from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security.jwt import decode_token
from app.repository.user_repository import UserRepository


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials | None = await super().__call__(request)
        if credentials is None:
            raise HTTPException(status_code=401, detail="Invalid authorization header")

        try:
            payload = decode_token(credentials.credentials)
            email = payload.get("email")
            if not email:
                raise UnauthorizedError("Invalid token payload")

            db = SessionLocal()
            try:
                repository = UserRepository(db)
                user = repository.get_by_email(email)
                if user is None:
                    raise ForbiddenError("User not found for provided token")
            finally:
                db.close()

            return payload
        except HTTPException:
            raise
        except UnauthorizedError as exc:
            raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc
        except ForbiddenError as exc:
            raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc
