from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from app.controller.movie import MovieController
from app.dependencies.providers import get_movie_controller
from app.schemas.common import MessageResponse
from app.schemas.movie import MovieCreate, MovieFilterQuery, MovieResponse, MovieUpdate

movie_router = APIRouter(prefix="/movies", tags=["movies"])


@movie_router.get("", response_model=list[MovieResponse], status_code=status.HTTP_200_OK)
async def get_movies(
    controller: MovieController = Depends(get_movie_controller),
) -> list[MovieResponse]:
    return controller.get_movies()


@movie_router.get(
    "/search",
    response_model=list[MovieResponse],
    status_code=status.HTTP_200_OK,
)
async def get_movies_by_category(
    filters: Annotated[MovieFilterQuery, Depends()],
    controller: MovieController = Depends(get_movie_controller),
) -> list[MovieResponse]:
    return controller.get_movies_by_category(filters.category)


@movie_router.get(
    "/{id}",
    response_model=MovieResponse,
    status_code=status.HTTP_200_OK,
)
async def get_movie(
    id: Annotated[int, Path(ge=1, le=2000)],
    controller: MovieController = Depends(get_movie_controller),
) -> MovieResponse:
    return controller.get_movie_by_id(id)


@movie_router.post("", response_model=MovieResponse, status_code=status.HTTP_201_CREATED)
async def create_movie(
    movie: MovieCreate,
    controller: MovieController = Depends(get_movie_controller),
) -> MovieResponse:
    return controller.create_movie(movie)


@movie_router.post(
    "/all",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
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
)
async def update_movie(
    id: Annotated[int, Path(ge=1, le=2000)],
    movie: MovieUpdate,
    controller: MovieController = Depends(get_movie_controller),
) -> MovieResponse:
    return controller.update_movie(id, movie)


@movie_router.delete(
    "/{id}",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_movie(
    id: Annotated[int, Path(ge=1, le=2000)],
    controller: MovieController = Depends(get_movie_controller),
) -> MessageResponse:
    return controller.delete_movie(id)
