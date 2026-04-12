from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.controller.user import UserController
from app.dependencies.providers import get_current_user_email, get_user_controller
from app.schemas.common import ErrorResponse, MessageResponse
from app.schemas.user import UserCreate, UserResponse

user_router = APIRouter(tags=["Users"])


@user_router.post(
    "/create_user/",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear usuario",
    description=(
        "Crea un nuevo usuario en el sistema. "
        "Este endpoint requiere autenticacion con un token Bearer valido."
    ),
    response_description="Confirmacion de creacion del usuario.",
    responses={
        401: {
            "model": ErrorResponse,
            "description": "El token no fue enviado o no pudo validarse.",
        },
        403: {
            "model": ErrorResponse,
            "description": "El usuario autenticado no puede completar la operacion.",
        },
        409: {
            "model": ErrorResponse,
            "description": "Ya existe un usuario registrado con el correo indicado.",
        },
        500: {
            "model": ErrorResponse,
            "description": "Error interno no controlado al crear el usuario.",
        },
    },
)
async def create_user(
    user: UserCreate,
    current_user_email: str = Depends(get_current_user_email),
    controller: UserController = Depends(get_user_controller),
) -> MessageResponse:
    del current_user_email
    return controller.create_user(user)


@user_router.get(
    "/get_user",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
    description=(
        "Retorna todos los usuarios registrados en el sistema. "
        "Este endpoint requiere autenticacion con un token Bearer valido."
    ),
    response_description="Listado de usuarios registrados.",
    responses={
        401: {
            "model": ErrorResponse,
            "description": "El token no fue enviado o no pudo validarse.",
        },
        403: {
            "model": ErrorResponse,
            "description": "El usuario autenticado no puede consultar este recurso.",
        },
        500: {
            "model": ErrorResponse,
            "description": "Error interno no controlado al consultar usuarios.",
        },
    },
)
async def get_users(
    current_user_email: str = Depends(get_current_user_email),
    controller: UserController = Depends(get_user_controller),
) -> list[UserResponse]:
    del current_user_email
    return controller.get_users()


@user_router.get(
    "/get_user/",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario por correo",
    description=(
        "Busca un usuario por su correo electronico. "
        "Este endpoint requiere autenticacion con un token Bearer valido."
    ),
    response_description="Datos del usuario encontrado.",
    responses={
        401: {
            "model": ErrorResponse,
            "description": "El token no fue enviado o no pudo validarse.",
        },
        403: {
            "model": ErrorResponse,
            "description": "El usuario autenticado no puede consultar este recurso.",
        },
        404: {
            "model": ErrorResponse,
            "description": "No existe un usuario registrado con el correo indicado.",
        },
        500: {
            "model": ErrorResponse,
            "description": "Error interno no controlado al consultar el usuario.",
        },
    },
)
async def get_user_by_email(
    email: Annotated[
        str,
        Query(
            min_length=5,
            max_length=50,
            description="Correo electronico del usuario a consultar.",
            examples=["alexi@gmail.com"],
        ),
    ],
    current_user_email: str = Depends(get_current_user_email),
    controller: UserController = Depends(get_user_controller),
) -> UserResponse:
    del current_user_email
    return controller.get_user_by_email(email)
