from fastapi import HTTPException, status

from app.core.exceptions import AppException
from app.schemas.common import MessageResponse
from app.schemas.user import UserCreate, UserResponse
from app.service.user import UserService


class UserController:
    def __init__(self, service: UserService) -> None:
        self.service = service

    def create_user(self, user_data: UserCreate) -> MessageResponse:
        self._execute(lambda: self.service.create_user(user_data))
        return MessageResponse(message="The user has been created successfully")

    def get_users(self) -> list[UserResponse]:
        return self._execute(self.service.get_users)

    def get_user_by_email(self, email: str) -> UserResponse:
        return self._execute(lambda: self.service.get_user_by_email(email))

    def _execute(self, action):
        try:
            return action()
        except AppException as exc:
            raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            ) from exc
