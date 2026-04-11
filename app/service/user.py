from app.core.exceptions import ConflictError, NotFoundError
from app.repository.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def create_user(self, user_data: UserCreate) -> UserResponse:
        existing_user = self.repository.get_by_email(user_data.email)
        if existing_user is not None:
            raise ConflictError("User already exists")

        user = self.repository.create(user_data.model_dump())
        return UserResponse.model_validate(user)

    def get_users(self) -> list[UserResponse]:
        users = self.repository.get_all()
        return [UserResponse.model_validate(user) for user in users]

    def get_user_by_email(self, email: str) -> UserResponse:
        user = self.repository.get_by_email(email)
        if user is None:
            raise NotFoundError("User not found")
        return UserResponse.model_validate(user)
