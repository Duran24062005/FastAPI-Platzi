from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str = Field(min_length=5, max_length=50)


class UserCreate(UserBase):
    password: str = Field(min_length=5, max_length=50)

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "alexi@gmail.com",
                "password": "hxk65d",
            }
        }
    }


class UserResponse(UserBase):
    id: int

    model_config = {"from_attributes": True}


class UserFilterQuery(BaseModel):
    email: str = Field(min_length=5, max_length=50)


class LoginRequest(UserBase):
    password: str = Field(min_length=5, max_length=50)


class TokenResponse(BaseModel):
    token: str
