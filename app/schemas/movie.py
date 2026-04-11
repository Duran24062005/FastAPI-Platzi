from pydantic import BaseModel, Field

from app.core.constants import CURRENT_YEAR_LIMIT


class MovieBase(BaseModel):
    title: str = Field(min_length=5, max_length=50)
    overview: str = Field(
        default="Descripcion de la pelicula",
        min_length=15,
        max_length=1500,
    )
    year: int = Field(ge=1888, le=CURRENT_YEAR_LIMIT)
    rating: float = Field(ge=1, le=10)
    category: str = Field(min_length=3, max_length=15)


class MovieCreate(MovieBase):
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The Matrix",
                "overview": "Description of the movie",
                "year": 2024,
                "rating": 8.4,
                "category": "Accion",
            }
        }
    }


class MovieUpdate(MovieBase):
    pass


class MovieResponse(MovieBase):
    id: int

    model_config = {"from_attributes": True}


class MovieFilterQuery(BaseModel):
    category: str = Field(min_length=3, max_length=15)
