from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from config.database import Session
from model.movie_model import User2 as UserEntity
from pydantic import BaseModel, Field
from typing import List
from middlewares.jwt_bearer import JWTBearer
from fastapi.encoders import jsonable_encoder

user_router = APIRouter()

class UserModel(BaseModel):
    email: str = Field(min_length=5, max_length=50)
    password: str = Field(min_length=5, max_length=50)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "alexi@gmail.com",
                "password": "hxk65d"
            }
        }


@user_router.post('/create_user/', tags=['user'], status_code=201, response_model = dict, dependencies=[Depends(JWTBearer())])
async def create_user(user:UserModel) -> dict:
    db = Session()
    new_user = UserEntity(**user.dict())
    db.add(new_user)
    db.commit()
    db.close()
    return JSONResponse(status_code=201,content={'message': 'The User has been created successfully'})


@user_router.get('/get_user', tags=['user'], response_model=List[UserModel], status_code=200, dependencies=[Depends(JWTBearer())])
async def get_users() -> List[UserModel]:
    db = Session()
    resp = db.query(UserEntity).all()
    db.close()
    if resp:
        return JSONResponse(status_code=200, content=jsonable_encoder(resp))
    else:
        return JSONResponse(status_code=400, content={'message': 'detail not found'})
    

@user_router.get('/get_user/', tags=['user'], response_model = List[UserModel], dependencies=[Depends(JWTBearer())])
async def get_user_by_email(email: str) -> List[UserModel]:
    db = Session()
    resp = db.query(UserEntity).filter(UserEntity.email == email).first()
    db.close()
    if resp:
        return JSONResponse(status_code=200, content=jsonable_encoder(resp))
    else:
        return JSONResponse(status_code=400, content={'message': 'detail not found'})
    