from fastapi import HTTPException, status

from app.core.exceptions import AppException
from app.schemas.common import MessageResponse
from app.schemas.movie import MovieCreate, MovieResponse, MovieUpdate
from app.service.movie import MovieService


class MovieController:
    def __init__(self, service: MovieService) -> None:
        self.service = service

    def get_movies(self) -> list[MovieResponse]:
        return self._execute(self.service.get_movies)

    def get_movie_by_id(self, movie_id: int) -> MovieResponse:
        return self._execute(lambda: self.service.get_movie_by_id(movie_id))

    def get_movies_by_category(self, category: str) -> list[MovieResponse]:
        return self._execute(lambda: self.service.get_movies_by_category(category))

    def create_movie(self, movie_data: MovieCreate) -> MovieResponse:
        return self._execute(lambda: self.service.create_movie(movie_data))

    def create_movies(self, movies_data: list[MovieCreate]) -> MessageResponse:
        self._execute(lambda: self.service.create_movies(movies_data))
        return MessageResponse(message="All movies have been created successfully")

    def update_movie(self, movie_id: int, movie_data: MovieUpdate) -> MovieResponse:
        return self._execute(lambda: self.service.update_movie(movie_id, movie_data))

    def delete_movie(self, movie_id: int) -> MessageResponse:
        self._execute(lambda: self.service.delete_movie(movie_id))
        return MessageResponse(message="Deleted movie successfully")

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
