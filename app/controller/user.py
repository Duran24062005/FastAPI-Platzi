from fastapi import HTTPException, status

from app.core.exceptions import AppException
from app.schemas.common import MessageResponse
from app.schemas.user import AdminUserUpdate, UserResponse
from app.service.user import UserService


class UserController:
    def __init__(self, service: UserService) -> None:
        self.service = service

    def get_users(self) -> list[UserResponse]:
        return self._execute(self.service.get_users)

    def get_user_by_id(self, user_id: int) -> UserResponse:
        return self._execute(lambda: self.service.get_user_by_id(user_id))

    def update_user(self, user_id: int, user_data: AdminUserUpdate) -> UserResponse:
        return self._execute(lambda: self.service.update_user(user_id, user_data))

    def delete_user(self, user_id: int) -> MessageResponse:
        self._execute(lambda: self.service.delete_user(user_id))
        return MessageResponse(message="Deleted user successfully")

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
