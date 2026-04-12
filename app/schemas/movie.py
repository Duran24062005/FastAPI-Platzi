from pydantic import BaseModel, Field

from app.core.constants import CURRENT_YEAR_LIMIT


class MovieBase(BaseModel):
    title: str = Field(
        min_length=5,
        max_length=50,
        description="Titulo de la pelicula.",
        examples=["The Matrix"],
    )
    overview: str = Field(
        default="Descripcion de la pelicula",
        min_length=15,
        max_length=1500,
        description="Resumen o sinopsis de la pelicula.",
        examples=["A hacker discovers the nature of his reality and his role in the war against its controllers."],
    )
    year: int = Field(
        ge=1888,
        le=CURRENT_YEAR_LIMIT,
        description="Anio de lanzamiento de la pelicula.",
        examples=[1999],
    )
    rating: float = Field(
        ge=1,
        le=10,
        description="Calificacion de la pelicula en una escala de 1 a 10.",
        examples=[8.7],
    )
    category: str = Field(
        min_length=3,
        max_length=15,
        description="Categoria o genero principal de la pelicula.",
        examples=["Sci-Fi"],
    )


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
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The Matrix Reloaded",
                "overview": "Neo and his allies continue the fight against the machines.",
                "year": 2003,
                "rating": 7.2,
                "category": "Sci-Fi",
            }
        }
    }


class MovieResponse(MovieBase):
    id: int = Field(
        description="Identificador unico de la pelicula.",
        examples=[1],
    )

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "title": "The Matrix",
                "overview": "A hacker discovers the nature of his reality and his role in the war against its controllers.",
                "year": 1999,
                "rating": 8.7,
                "category": "Sci-Fi",
            }
        },
    }


class MovieFilterQuery(BaseModel):
    category: str = Field(
        min_length=3,
        max_length=15,
        description="Categoria utilizada para filtrar peliculas.",
        examples=["Sci-Fi"],
    )
