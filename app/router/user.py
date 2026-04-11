from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.controller.user import UserController
from app.dependencies.providers import get_current_user_email, get_user_controller
from app.schemas.common import MessageResponse
from app.schemas.user import UserCreate, UserFilterQuery, UserResponse

user_router = APIRouter(tags=["user"])


@user_router.post(
    "/create_user/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user_email)],
)
async def create_user(
    user: UserCreate,
    controller: UserController = Depends(get_user_controller),
) -> MessageResponse:
    return controller.create_user(user)


@user_router.get(
    "/get_user",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user_email)],
)
async def get_users(
    controller: UserController = Depends(get_user_controller),
) -> list[UserResponse]:
    return controller.get_users()


@user_router.get(
    "/get_user/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_user_email)],
)
async def get_user_by_email(
    filters: Annotated[UserFilterQuery, Depends()],
    controller: UserController = Depends(get_user_controller),
) -> UserResponse:
    return controller.get_user_by_email(filters.email)
