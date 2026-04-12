from app.core.exceptions import ConflictError, NotFoundError
from app.repository.user_repository import UserRepository
from app.schemas.user import AdminUserUpdate, UserResponse


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def get_users(self) -> list[UserResponse]:
        users = self.repository.get_all()
        return [UserResponse.model_validate(user) for user in users]

    def get_user_by_id(self, user_id: int) -> UserResponse:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found")
        return UserResponse.model_validate(user)

    def update_user(self, user_id: int, user_data: AdminUserUpdate) -> UserResponse:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found")

        existing_user = self.repository.get_by_email(user_data.email)
        if existing_user is not None and existing_user.id != user_id:
            raise ConflictError("User already exists")

        updated_user = self.repository.update(user, user_data.model_dump())
        return UserResponse.model_validate(updated_user)

    def delete_user(self, user_id: int) -> None:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError("User not found")

        self.repository.delete(user)
