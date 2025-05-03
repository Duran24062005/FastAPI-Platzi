from fastapi import APIRouter, Path, Depends
from fastapi.responses import JSONResponse
from config.database import Session
from model.movie_model import Movie as MoviEntity
from pydantic import BaseModel, Field
from typing import List
from middlewares.jwt_bearer import JWTBearer
from fastapi.encoders import jsonable_encoder
from service.movie import MovieService

movie_router = APIRouter()


class Movie(BaseModel):
    title: str = Field(min_length=5, max_length=50)
    overview: str = Field(default='Descripción de la pelicula', min_length=15, max_length=1500)
    year: int = Field(le=2024)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=5, max_length=15)

    class Config:
        json_schema_extra = {
            "example":{
                'title': 'The Matrix',
                'overview': 'Description of the movie',
                'year': 2024,
                'rating': 8.4,
                'category': 'Acción'
            }
        }



@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200)
async def get_movies() -> List[Movie]:
    db = Session()
    resp = MovieService(db).get_movies()
    db.close()
    return JSONResponse(status_code=200, content=jsonable_encoder(resp))



@movie_router.get('/movies/{id}', tags=['movies'], response_model = Movie, status_code=200)
async def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    resp = db.query(MoviEntity).filter(MoviEntity.id == id).first()
    db.close()
    if resp:
        return JSONResponse(status_code=200, content=jsonable_encoder(resp))
    else:
        return JSONResponse(status_code=404,content={'message': 'Movie not found'})



@movie_router.get('/movies/', tags=['movies'], response_model = List[Movie])
async def get_movies_by_category(category: str) -> List[Movie]:
    db = Session()
    resp = db.query(MoviEntity).filter(MoviEntity.category == category).all()
    db.close()
    if resp:
        return JSONResponse(status_code=200, content=jsonable_encoder(resp))
    else:
        return JSONResponse(status_code=400, content={'message': 'detail not found'})
    


@movie_router.post('/movies/', tags=['movies'], response_model = dict, status_code=201)
async def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MoviEntity(**movie.model_dump())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201,content={'message': 'The movie has been created successfully'})




@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
async def update_movie(id: int, movie: Movie) -> dict:
    db = Session()
    resp = db.query(MoviEntity).filter(MoviEntity.id == id).first()
    if resp:
        resp.title = movie.title
        resp.overview = movie.overview
        resp.year = movie.year
        resp.rating = movie.rating
        resp.category = movie.category
        db.commit()
        db.close()
        return JSONResponse(status_code=200, content={'message': 'The movie has been updated successfully'})
    else:
        return JSONResponse(content={'message': 'Fail, this movie does not exist'})



@movie_router.delete('/movies/{id}', tags=['movies'], status_code=200)
async def delete_movie(id: int):
    db = Session()
    resp = db.query(MoviEntity).filter(MoviEntity.id == id).first()
    if resp:
        db.delete(resp)
        db.commit()
        db.close()
        return JSONResponse(status_code=200, content={'message': 'Deleted movie successfully'})
    else:
        return JSONResponse(content={'message': 'Fail, this movie does not exist'})