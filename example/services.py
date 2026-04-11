from example.db import db_movie, db_user


def get_movie_by_id(movie_id: int):
    for movie in db_movie:
        if movie["id"] == movie_id:
            return movie
    return None


def get_movie_by_category(category: str, year: int | None = None):
    movies = [movie for movie in db_movie if movie["category"] == category]
    if year is not None:
        movies = [movie for movie in movies if int(movie["year"]) == year]
    return movies


def check_if_movie_exist(movie_id: int, title: str):
    for movie in db_movie:
        if movie["id"] == movie_id or movie["title"] == title:
            return movie
    return None


def verify_credentials(user):
    email = getattr(user, "email", None)
    password = getattr(user, "password", None)
    return any(item["email"] == email and item["password"] == password for item in db_user)
