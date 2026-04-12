from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str = Field(
        min_length=5,
        max_length=50,
        description="Correo electronico del usuario.",
        examples=["alexi@gmail.com"],
    )


class UserCreate(UserBase):
    password: str = Field(
        min_length=5,
        max_length=50,
        description="Contrasena del usuario.",
        examples=["hxk65d"],
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "alexi@gmail.com",
                "password": "hxk65d",
            }
        }
    }


class UserResponse(UserBase):
    id: int = Field(
        description="Identificador unico del usuario.",
        examples=[1],
    )

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "email": "alexi@gmail.com",
            }
        },
    }


class UserFilterQuery(BaseModel):
    email: str = Field(
        min_length=5,
        max_length=50,
        description="Correo electronico utilizado para buscar un usuario.",
        examples=["alexi@gmail.com"],
    )


class LoginRequest(UserBase):
    password: str = Field(
        min_length=5,
        max_length=50,
        description="Contrasena del usuario para autenticarse.",
        examples=["hxk65d"],
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "alexi@gmail.com",
                "password": "hxk65d",
            }
        }
    }


class TokenResponse(BaseModel):
    token: str = Field(
        description="Token JWT que debe enviarse en el header Authorization como Bearer token.",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )
