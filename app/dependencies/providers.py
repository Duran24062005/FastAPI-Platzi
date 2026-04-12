from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.controller.auth import AuthController
from app.controller.movie import MovieController
from app.controller.user import UserController
from app.core.exceptions import ForbiddenError
from app.core.security.bearer import JWTBearer
from app.model.user_model import User
from app.repository.movie_repository import MovieRepository
from app.repository.user_repository import UserRepository
from app.service.auth import AuthService
from app.service.movie import MovieService
from app.service.user import UserService


async def get_db() -> AsyncGenerator[Session, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_movie_controller(db: Session = Depends(get_db)) -> MovieController:
    repository = MovieRepository(db)
    service = MovieService(repository)
    return MovieController(service)


async def get_user_controller(db: Session = Depends(get_db)) -> UserController:
    repository = UserRepository(db)
    service = UserService(repository)
    return UserController(service)


async def get_auth_controller(db: Session = Depends(get_db)) -> AuthController:
    repository = UserRepository(db)
    service = AuthService(repository)
    return AuthController(service)


async def get_current_user(
    token_payload: dict = Depends(JWTBearer()),
    db: Session = Depends(get_db),
) -> User:
    repository = UserRepository(db)
    user = repository.get_by_email(token_payload["email"])
    if user is None:
        raise ForbiddenError("User not found for provided token")
    return user


async def get_current_user_email(
    current_user: User = Depends(get_current_user),
) -> str:
    return current_user.email


async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != "admin":
        raise ForbiddenError("Admin access required")
    return current_user
