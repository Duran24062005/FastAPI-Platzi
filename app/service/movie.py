from app.core.exceptions import NotFoundError, ValidationAppError
from app.repository.movie_repository import MovieRepository
from app.schemas.movie import MovieCreate, MovieResponse, MovieUpdate


class MovieService:
    def __init__(self, repository: MovieRepository) -> None:
        self.repository = repository

    def get_movies(self) -> list[MovieResponse]:
        movies = self.repository.get_all()
        return [MovieResponse.model_validate(movie) for movie in movies]

    def get_movie_by_id(self, movie_id: int) -> MovieResponse:
        movie = self.repository.get_by_id(movie_id)
        if movie is None:
            raise NotFoundError("Movie not found")
        return MovieResponse.model_validate(movie)

    def get_movies_by_category(self, category: str) -> list[MovieResponse]:
        movies = self.repository.get_by_category(category)
        if not movies:
            raise NotFoundError("Movies not found for the provided category")
        return [MovieResponse.model_validate(movie) for movie in movies]

    def create_movie(self, movie_data: MovieCreate) -> MovieResponse:
        movie = self.repository.create(movie_data.model_dump())
        return MovieResponse.model_validate(movie)

    def create_movies(self, movies_data: list[MovieCreate]) -> list[MovieResponse]:
        if not movies_data:
            raise ValidationAppError("At least one movie is required")

        try:
            movies = self.repository.create_many(
                [movie.model_dump() for movie in movies_data]
            )
        except Exception as exc:
            self.repository.rollback()
            raise ValidationAppError(f"Unable to create movies: {exc}") from exc

        return [MovieResponse.model_validate(movie) for movie in movies]

    def update_movie(self, movie_id: int, movie_data: MovieUpdate) -> MovieResponse:
        movie = self.repository.get_by_id(movie_id)
        if movie is None:
            raise NotFoundError("Movie not found")

        updated_movie = self.repository.update(movie, movie_data.model_dump())
        return MovieResponse.model_validate(updated_movie)

    def delete_movie(self, movie_id: int) -> None:
        movie = self.repository.get_by_id(movie_id)
        if movie is None:
            raise NotFoundError("Movie not found")

        self.repository.delete(movie)
