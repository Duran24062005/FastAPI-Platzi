from app.core.exceptions import ConflictError, ForbiddenError, UnauthorizedError
from app.core.security.jwt import create_token
from app.repository.user_repository import UserRepository
from app.schemas.user import LoginRequest, UserRegisterRequest, UserResponse, UserRole


class AuthService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def register(self, user_data: UserRegisterRequest) -> UserResponse:
        existing_user = self.repository.get_by_email(user_data.email)
        if existing_user is not None:
            raise ConflictError("User already exists")

        user = self.repository.create(
            {
                **user_data.model_dump(),
                "role": UserRole.USER.value,
            }
        )
        return UserResponse.model_validate(user)

    def login(self, credentials: LoginRequest) -> str:
        user = self.repository.get_by_email(credentials.email)
        if user is None:
            raise UnauthorizedError("Invalid credentials")

        if user.password != credentials.password:
            raise ForbiddenError("Invalid credentials")

        return create_token({"email": user.email, "role": user.role})
