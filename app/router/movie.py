from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, status

from app.controller.movie import MovieController
from app.dependencies.providers import get_movie_controller
from app.schemas.common import ErrorResponse, MessageResponse
from app.schemas.movie import MovieCreate, MovieResponse, MovieUpdate

movie_router = APIRouter(prefix="/movies", tags=["Movies"])


@movie_router.get(
    "",
    response_model=list[MovieResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar peliculas",
    description="Retorna todas las peliculas registradas en el sistema.",
    response_description="Listado completo de peliculas.",
    responses={
        500: {
            "model": ErrorResponse,
            "description": "Error interno no controlado al consultar las peliculas.",
        },
    },
)
async def get_movies(
    controller: MovieController = Depends(get_movie_controller),
) -> list[MovieResponse]:
    return controller.get_movies()


@movie_router.get(
    "/search",
    response_model=list[MovieResponse],
    status_code=status.HTTP_200_OK,
    summary="Buscar peliculas por categoria",
    description="Retorna las peliculas que pertenecen a una categoria especifica.",
    response_description="Listado de peliculas que coinciden con la categoria solicitada.",
    responses={
        404: {
            "model": ErrorResponse,
            "description": "No existen peliculas registradas para la categoria enviada.",
        },
        500: {
            "model": ErrorResponse,
            "description": "Error interno no controlado al filtrar peliculas.",
        },
    },
)
async def get_movies_by_category(
    category: Annotated[
        str,
        Query(
            min_length=3,
            max_length=15,
            description="Categoria usada para filtrar las peliculas.",
            examples=["Sci-Fi"],
        ),
    ],
    controller: MovieController = Depends(get_movie_controller),
) -> list[MovieResponse]:
    return controller.get_movies_by_category(category)


@movie_router.get(
    "/{id}",
    response_model=MovieResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener pelicula por ID",
    description="Retorna la informacion detallada de una pelicula a partir de su identificador.",
    response_description="Detalle de la pelicula encontrada.",
    responses={
        404: {
            "model": ErrorResponse,
            "description": "No existe una pelicula con el identificador indicado.",
        },
        500: {
            "model": ErrorResponse,
            "description": "Error interno no controlado al consultar la pelicula.",
        },
    },
)
async def get_movie(
    id: Annotated[
        int,
        Path(
            ge=1,
            le=2000,
            description="Identificador unico de la pelicula.",
            examples=[1],
        ),
    ],
    controller: MovieController = Depends(get_movie_controller),
) -> MovieResponse:
    return controller.get_movie_by_id(id)


@movie_router.post(
    "",
    response_model=MovieResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear pelicula",
    description="Crea una nueva pelicula con la informacion enviada en el cuerpo de la solicitud.",
    response_description="Pelicula creada correctamente.",
    responses={
        422: {
            "description": "El cuerpo de la solicitud no cumple con las validaciones definidas.",
        },
        500: {
            "model": ErrorResponse,
            "description": "Error interno no controlado al crear la pelicula.",
        },
    },
)
async def create_movie(
    movie: MovieCreate,
    controller: MovieController = Depends(get_movie_controller),
) -> MovieResponse:
    return controller.create_movie(movie)


@movie_router.post(
    "/all",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear multiples peliculas",
    description=(
        "Crea varias peliculas en una sola operacion. "
        "El cuerpo debe contener al menos un elemento valido."
    ),
    response_description="Confirmacion de creacion masiva de peliculas.",
    responses={
        400: {
            "model": ErrorResponse,
            "description": "La solicitud no contiene peliculas validas para crear.",
        },
        422: {
            "description": "Uno o mas elementos del cuerpo no cumplen las validaciones definidas.",
        },
        500: {
            "model": ErrorResponse,
            "description": "Error interno no controlado durante la creacion masiva.",
        },
    },
)
async def create_movies(
    movies: list[MovieCreate],
    controller: MovieController = Depends(get_movie_controller),
) -> MessageResponse:
    return controller.create_movies(movies)


@movie_router.put(
    "/{id}",
    response_model=MovieResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar pelicula",
    description="Actualiza la informacion de una pelicula existente a partir de su identificador.",
    response_description="Pelicula actualizada correctamente.",
    responses={
        404: {
            "model": ErrorResponse,
            "description": "No existe una pelicula con el identificador indicado.",
        },
        422: {
            "description": "El cuerpo de la solicitud no cumple con las validaciones definidas.",
        },
        500: {
            "model": ErrorResponse,
            "description": "Error interno no controlado al actualizar la pelicula.",
        },
    },
)
async def update_movie(
    id: Annotated[
        int,
        Path(
            ge=1,
            le=2000,
            description="Identificador unico de la pelicula a actualizar.",
            examples=[1],
        ),
    ],
    movie: MovieUpdate,
    controller: MovieController = Depends(get_movie_controller),
) -> MovieResponse:
    return controller.update_movie(id, movie)


@movie_router.delete(
    "/{id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Eliminar pelicula",
    description="Elimina una pelicula existente a partir de su identificador.",
    response_description="Confirmacion de eliminacion de la pelicula.",
    responses={
        404: {
            "model": ErrorResponse,
            "description": "No existe una pelicula con el identificador indicado.",
        },
        500: {
            "model": ErrorResponse,
            "description": "Error interno no controlado al eliminar la pelicula.",
        },
    },
)
async def delete_movie(
    id: Annotated[
        int,
        Path(
            ge=1,
            le=2000,
            description="Identificador unico de la pelicula a eliminar.",
            examples=[1],
        ),
    ],
    controller: MovieController = Depends(get_movie_controller),
) -> MessageResponse:
    return controller.delete_movie(id)
