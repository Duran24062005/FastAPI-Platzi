from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security.jwt import create_token
from app.repository.user_repository import UserRepository
from app.schemas.user import LoginRequest


class AuthService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def login(self, credentials: LoginRequest) -> str:
        user = self.repository.get_by_email(credentials.email)
        if user is None:
            raise UnauthorizedError("Invalid credentials")

        if user.password != credentials.password:
            raise ForbiddenError("Invalid credentials")

        return create_token({"email": user.email})
