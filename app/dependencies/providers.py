from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.controller.auth import AuthController
from app.controller.movie import MovieController
from app.controller.user import UserController
from app.core.security.bearer import JWTBearer
from app.repository.movie_repository import MovieRepository
from app.repository.user_repository import UserRepository
from app.service.auth import AuthService
from app.service.movie import MovieService
from app.service.user import UserService


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_movie_controller(db: Session = Depends(get_db)) -> MovieController:
    repository = MovieRepository(db)
    service = MovieService(repository)
    return MovieController(service)


def get_user_controller(db: Session = Depends(get_db)) -> UserController:
    repository = UserRepository(db)
    service = UserService(repository)
    return UserController(service)


def get_auth_controller(db: Session = Depends(get_db)) -> AuthController:
    repository = UserRepository(db)
    service = AuthService(repository)
    return AuthController(service)


def get_current_user_email(
    token_payload: dict = Depends(JWTBearer()),
) -> str:
    return token_payload["email"]
