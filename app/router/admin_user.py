from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.controller.user import UserController
from app.dependencies.providers import get_current_admin_user, get_user_controller
from app.model.user_model import User
from app.schemas.common import ErrorResponse, MessageResponse
from app.schemas.user import AdminUserUpdate, UserResponse

admin_user_router = APIRouter(prefix="/users", tags=["Admin Users"])


@admin_user_router.get(
    "",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar usuarios",
    description="Retorna todos los usuarios registrados. Requiere un usuario autenticado con rol admin.",
    response_description="Listado de usuarios registrados.",
    responses={
        401: {
            "model": ErrorResponse,
            "description": "El token no fue enviado o no pudo validarse.",
        },
        403: {
            "model": ErrorResponse,
            "description": "El usuario autenticado no tiene permisos de administrador.",
        },
        500: {
            "model": ErrorResponse,
            "description": "Error interno no controlado al consultar usuarios.",
        },
    },
)
async def get_users(
    current_admin_user: User = Depends(get_current_admin_user),
    controller: UserController = Depends(get_user_controller),
) -> list[UserResponse]:
    del current_admin_user
    return controller.get_users()


@admin_user_router.get(
    "/{id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario por ID",
    description="Retorna el detalle de un usuario a partir de su identificador. Requiere rol admin.",
    response_description="Detalle del usuario encontrado.",
    responses={
        401: {
            "model": ErrorResponse,
            "description": "El token no fue enviado o no pudo validarse.",
        },
        403: {
            "model": ErrorResponse,
            "description": "El usuario autenticado no tiene permisos de administrador.",
        },
        404: {
            "model": ErrorResponse,
            "description": "No existe un usuario con el identificador indicado.",
        },
        500: {
            "model": ErrorResponse,
            "description": "Error interno no controlado al consultar el usuario.",
        },
    },
)
async def get_user(
    id: Annotated[
        int,
        Path(
            ge=1,
            description="Identificador unico del usuario.",
            examples=[1],
        ),
    ],
    current_admin_user: User = Depends(get_current_admin_user),
    controller: UserController = Depends(get_user_controller),
) -> UserResponse:
    del current_admin_user
    return controller.get_user_by_id(id)


@admin_user_router.put(
    "/{id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario",
    description="Actualiza email, contrasena y rol de un usuario existente. Requiere rol admin.",
    response_description="Usuario actualizado correctamente.",
    responses={
        401: {
            "model": ErrorResponse,
            "description": "El token no fue enviado o no pudo validarse.",
        },
        403: {
            "model": ErrorResponse,
            "description": "El usuario autenticado no tiene permisos de administrador.",
        },
        404: {
            "model": ErrorResponse,
            "description": "No existe un usuario con el identificador indicado.",
        },
        409: {
            "model": ErrorResponse,
            "description": "El email enviado ya pertenece a otro usuario.",
        },
        422: {
            "description": "El cuerpo de la solicitud no cumple con las validaciones definidas.",
        },
        500: {
            "model": ErrorResponse,
            "description": "Error interno no controlado al actualizar el usuario.",
        },
    },
)
async def update_user(
    id: Annotated[
        int,
        Path(
            ge=1,
            description="Identificador unico del usuario a actualizar.",
            examples=[1],
        ),
    ],
    user: AdminUserUpdate,
    current_admin_user: User = Depends(get_current_admin_user),
    controller: UserController = Depends(get_user_controller),
) -> UserResponse:
    del current_admin_user
    return controller.update_user(id, user)


@admin_user_router.delete(
    "/{id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Eliminar usuario",
    description="Elimina un usuario existente a partir de su identificador. Requiere rol admin.",
    response_description="Confirmacion de eliminacion del usuario.",
    responses={
        401: {
            "model": ErrorResponse,
            "description": "El token no fue enviado o no pudo validarse.",
        },
        403: {
            "model": ErrorResponse,
            "description": "El usuario autenticado no tiene permisos de administrador.",
        },
        404: {
            "model": ErrorResponse,
            "description": "No existe un usuario con el identificador indicado.",
        },
        500: {
            "model": ErrorResponse,
            "description": "Error interno no controlado al eliminar el usuario.",
        },
    },
)
async def delete_user(
    id: Annotated[
        int,
        Path(
            ge=1,
            description="Identificador unico del usuario a eliminar.",
            examples=[1],
        ),
    ],
    current_admin_user: User = Depends(get_current_admin_user),
    controller: UserController = Depends(get_user_controller),
) -> MessageResponse:
    del current_admin_user
    return controller.delete_user(id)
