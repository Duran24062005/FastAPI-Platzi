from pydantic import BaseModel, Field


class MessageResponse(BaseModel):
    message: str = Field(
        description="Mensaje descriptivo del resultado de la operacion.",
        examples=["The user has been created successfully"],
    )


class ErrorResponse(BaseModel):
    detail: str = Field(
        description="Detalle legible del error retornado por la API.",
        examples=["Movie not found"],
    )
