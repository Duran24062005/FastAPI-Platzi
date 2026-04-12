from fastapi import APIRouter, Depends, status

from app.controller.auth import AuthController
from app.dependencies.providers import get_auth_controller
from app.schemas.common import ErrorResponse
from app.schemas.user import LoginRequest, TokenResponse, UserRegisterRequest, UserResponse

auth_router = APIRouter(
    tags=["Auth"],
    prefix="",
)


@auth_router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar usuario",
    description=(
        "Registra un nuevo usuario de forma publica. "
        "Los usuarios creados por esta ruta reciben el rol user por defecto."
    ),
    response_description="Usuario registrado correctamente.",
    responses={
        409: {
            "model": ErrorResponse,
            "description": "Ya existe un usuario registrado con el correo indicado.",
        },
        500: {
            "model": ErrorResponse,
            "description": "Error interno no controlado durante el registro.",
        },
    },
)
async def register(
    user: UserRegisterRequest,
    controller: AuthController = Depends(get_auth_controller),
) -> UserResponse:
    return controller.register(user)


@auth_router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Iniciar sesion",
    description=(
        "Autentica un usuario con su correo y contrasena. "
        "Si las credenciales son validas, retorna un token JWT para consumir "
        "los endpoints protegidos."
    ),
    response_description="Token JWT generado para el usuario autenticado.",
    responses={
        401: {
            "model": ErrorResponse,
            "description": "No fue posible autenticar al usuario con las credenciales enviadas.",
        },
        403: {
            "model": ErrorResponse,
            "description": "Las credenciales son invalidas para acceder al recurso.",
        },
        500: {
            "model": ErrorResponse,
            "description": "Error interno no controlado durante el inicio de sesion.",
        },
    },
)
async def login(
    credentials: LoginRequest,
    controller: AuthController = Depends(get_auth_controller),
) -> TokenResponse:
    return controller.login(credentials)
