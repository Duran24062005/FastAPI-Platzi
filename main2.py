from fastapi import FastAPI, Body
from  fastapi.responses import HTMLResponse
from db import db_movie
from service import get_movie_by_id, get_movie_by_category, check_if_movie_exist


app = FastAPI()
app.title = 'Mi app con FastAPI'



@app.get("/", tags=['Home'])
def message():
    return HTMLResponse('<h1>¡Hello world!<h1>')

@app.get('/movies', tags=['movies'])
def get_movies():
    return db_movie

@app.get('/movies/{id}', tags=['movies'])
def get_movie(id: int):
    resp = get_movie_by_id(id)
    if resp:
        return resp
    else:
        return {'message': 'Movie not found'}

@app.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str, year: int):
    resp = get_movie_by_category(category, year)
    if resp:
        return resp
    else:
        return {'message': 'detail not found'}
    

@app.post('/movies/', tags=['movies'])
def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    if check_if_movie_exist(id, title) is not None:
        return {'message': 'Movie already exist'}
    else:
        db_movie.append({
            'id' : id, 
            'title': title, 
            'overview': overview, 
            'year': year, 
            'rating': rating, 
            'category': category
        })
    return db_movie

@app.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    if get_movie_by_id(id):
        item = get_movie_by_id(id)
        item['title'] = title,
        item['everview'] = overview,
        item['year'] = year,
        item['rating'] = rating,
        item['category'] = category,
        return item
    else:
        return {'message': 'Fail, this movie does not exist'}
    
@app.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
    if get_movie_by_id(id):
        item = get_movie_by_id(id)
        db_movie.remove(item)
        return item
    else:
        return {'message': 'Fail, this movie does not exist'}
 