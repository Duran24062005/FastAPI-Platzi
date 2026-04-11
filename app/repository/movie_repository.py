from sqlalchemy.orm import Session

from app.model.movie_model import Movie


class MovieRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[Movie]:
        return self.db.query(Movie).all()

    def get_by_id(self, movie_id: int) -> Movie | None:
        return self.db.query(Movie).filter(Movie.id == movie_id).first()

    def get_by_category(self, category: str) -> list[Movie]:
        return self.db.query(Movie).filter(Movie.category == category).all()

    def create(self, movie_data: dict) -> Movie:
        movie = Movie(**movie_data)
        self.db.add(movie)
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def create_many(self, movies_data: list[dict]) -> list[Movie]:
        movies = [Movie(**movie_data) for movie_data in movies_data]
        self.db.add_all(movies)
        self.db.commit()
        for movie in movies:
            self.db.refresh(movie)
        return movies

    def update(self, movie: Movie, movie_data: dict) -> Movie:
        for field, value in movie_data.items():
            setattr(movie, field, value)
        self.db.commit()
        self.db.refresh(movie)
        return movie

    def delete(self, movie: Movie) -> None:
        self.db.delete(movie)
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()
