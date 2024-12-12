from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from jwt_manager import create_token
from config.database import engine, Base
from middlewares.error import ErrorHandler
from router.user import UserModel
from router.user import user_router
from router.movie import movie_router



app = FastAPI()
app.title = '⚙️Mi app con FastAPI🔧'
app.description = "🛠️My firstApp in FasAPI whit Platzi🛠️"
app.version = '0.1.0'

app.add_middleware(ErrorHandler)

app.include_router(user_router)
app.include_router(movie_router)

Base.metadata.create_all(bind=engine)





@app.get("/", tags=['Home'])
async def message():
    return HTMLResponse('<h1>¡Hello world!<h1>')


@app.post("/Login", tags=['auth'])
async def login(user: UserModel):
        token: str = create_token(user.model_dump())
        return JSONResponse(content=token, status_code=200)
        