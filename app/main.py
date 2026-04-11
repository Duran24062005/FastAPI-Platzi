import os

from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse

from app.config.config import app_config
from app.config.database import Base, engine
from app.middlewares.cors import app_cors
from app.middlewares.error import register_exception_handlers
from app.router.auth import auth_router
from app.router.movie import movie_router
from app.router.user import user_router

app = FastAPI(
    title=app_config["APP_NAME"],
    description=app_config["DESCRIPTION"],
    version=app_config["VERSION"],
    docs_url="/",
)

app_cors(app)
register_exception_handlers(app)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(movie_router)

_db_initialized = False


@app.on_event("startup")
async def startup_event() -> None:
    global _db_initialized
    if _db_initialized:
        return

    Base.metadata.create_all(bind=engine)
    _db_initialized = True


@app.get("/health", tags=["Health"])
async def health_check() -> JSONResponse:
    database_engine = "PostgreSQL" if os.getenv("PGHOST") else "SQLite"
    return JSONResponse(
        content={
            "status": "ok",
            "version": app.version,
            "database": database_engine,
            "db_initialized": _db_initialized,
        },
        status_code=200,
    )


@app.get("/home", tags=["Home"])
async def message() -> HTMLResponse:
    return HTMLResponse("<h1>Hello world!</h1>")


handler = app
