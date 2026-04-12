from fastapi import HTTPException, status

from app.core.exceptions import AppException
from app.schemas.user import LoginRequest, TokenResponse, UserRegisterRequest, UserResponse
from app.service.auth import AuthService


class AuthController:
    def __init__(self, service: AuthService) -> None:
        self.service = service

    def register(self, user_data: UserRegisterRequest) -> UserResponse:
        try:
            return self.service.register(user_data)
        except AppException as exc:
            raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            ) from exc

    def login(self, credentials: LoginRequest) -> TokenResponse:
        try:
            token = self.service.login(credentials)
            return TokenResponse(token=token)
        except AppException as exc:
            raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            ) from exc
