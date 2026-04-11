from fastapi import APIRouter, Depends, status

from app.controller.auth import AuthController
from app.dependencies.providers import get_auth_controller
from app.schemas.user import LoginRequest, TokenResponse

auth_router = APIRouter(tags=["auth"])


@auth_router.post("/Login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(
    credentials: LoginRequest,
    controller: AuthController = Depends(get_auth_controller),
) -> TokenResponse:
    return controller.login(credentials)
