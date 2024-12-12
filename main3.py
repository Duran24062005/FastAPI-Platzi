from fastapi import FastAPI, HTTPException, Path, Query, Request, Depends
from  fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security.http import HTTPAuthorizationCredentials
from db import db_movie, db_user
from service import get_movie_by_id, get_movie_by_category, check_if_movie_exist, verify_credentials
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, verify_token
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from model.movie_model import Movie as MoviEntity
from model.movie_model import User2 as UserEntity
from fastapi.encoders import jsonable_encoder


app = FastAPI()
app.title = 'Mi app con FastAPI'
app.version = '0.1.0'

Base.metadata.create_all(bind=engine)



class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = verify_token(auth.credentials)
        if data['email'] != 'alexi@gmail.com':
            raise HTTPException(status_code=403, detail='the credential are invalid')


class UserModel(BaseModel):
    email: str = Field(min_length=5, max_length=50)
    password: str = Field(min_length=5, max_length=50)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "alexi@gmail.com",
                "password": "123456@JJ"
            }
        }

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


@app.get("/", tags=['Home'])
async def message():
    return HTMLResponse('<h1>¡Hello world!<h1>')


@app.post("/Login", tags=['auth'])
async def login(user: UserModel):
    if verify_credentials(user):
        token: str = create_token(user.dict())
        return JSONResponse(content=token, status_code=200)




@app.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
async def get_movies() -> List[Movie]:
    db = Session()
    resp = db.query(MoviEntity).all()
    db.close()
    return JSONResponse(status_code=200, content=jsonable_encoder(resp))



@app.get('/movies/{id}', tags=['movies'], response_model = Movie, status_code=200)
async def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    resp = get_movie_by_id(id)
    if resp:
        return JSONResponse(status_code=200, content=resp)
    else:
        return JSONResponse(status_code=404,content={'message': 'Movie not found'})



@app.get('/movies/', tags=['movies'], response_model = List[Movie])
async def get_movies_by_category(category: str = Query(ge=5, le=15)) -> List[Movie]:
    resp = get_movie_by_category(category)
    if resp:
        return JSONResponse(content=resp)
    else:
        return JSONResponse(content={'message': 'detail not found'})
    


@app.post('/movies/', tags=['movies'], response_model = dict, status_code=201)
async def create_movie(movie: Movie) -> dict:
    db = Session()
    new_movie = MoviEntity(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201,content={'message': 'The movie has been created successfully'})




@app.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
async def update_movie(id: int, movie: Movie) -> dict:
    if get_movie_by_id(id):
        item = get_movie_by_id(id)
        item['title'] = movie.title
        item['everview'] = movie.overview
        item['year'] = movie.year
        item['rating'] = movie.rating
        item['category'] = movie.category
        return JSONResponse(status_code=200, content={'message': 'The movie has been updated successfully'})
    else:
        return JSONResponse(content={'message': 'Fail, this movie does not exist'})



@app.delete('/movies/{id}', tags=['movies'], status_code=200)
async def delete_movie(id: int):
    if get_movie_by_id(id):
        item = get_movie_by_id(id)
        db_movie.remove(item)
        return JSONResponse(status_code=200, content={'message': 'Deleted movie successfully'})
    else:
        return JSONResponse(content={'message': 'Fail, this movie does not exist'})
    


@app.get('/hi', tags=['auth'], response_model=dict, dependencies=[Depends(JWTBearer())])
async def index(name) -> dict:
    return JSONResponse(content = {'message': f'hellow {name},this is an API for example'})


@app.post('/create_user/', tags=['user'], status_code=201, response_model = dict)
async def create_user(user:UserModel) -> dict:
    db = Session()
    new_user = UserEntity(**user.dict())
    db.add(new_user)
    db.commit()
    return JSONResponse(status_code=201,content={'message': 'The User has been created successfully'})


@app.get('/get_user', tags=['user'], response_model=List[UserModel], status_code=200)
async def get_users() -> List[UserModel]:
    db = Session()
    resp = db.query(UserEntity).all()
    db.close()
    return JSONResponse(status_code=200, content=jsonable_encoder(resp))