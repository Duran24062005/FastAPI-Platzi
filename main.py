from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from jwt_manager import create_token
from middlewares.error import ErrorHandler
from middlewares.cors import app_cors
from router.user import UserModel
from router.user import user_router
from router.movie import movie_router

app = FastAPI(
    docs_url = "/"
)
app.title = '⚙️Mi app con FastAPI🔧'
app.description = "🛠️My firstApp in FastAPI with Platzi🛠️"
app.version = '0.1.0'


# Cors Middleware
app_cors(app)

app.add_middleware(ErrorHandler)

app.include_router(user_router)
app.include_router(movie_router)

# Variable para trackear si las tablas ya se crearon
_db_initialized = False

@app.on_event("startup")
async def startup_event():
    """Inicializar base de datos en el primer request"""
    global _db_initialized
    if not _db_initialized:
        try:
            from config.database import engine, Base
            print("🔧 Creando tablas en la base de datos...")
            Base.metadata.create_all(bind=engine)
            print("✅ Tablas creadas exitosamente")
            _db_initialized = True
        except Exception as e:
            print(f"❌ Error al crear tablas: {e}")
            # No lanzar excepción para permitir que la app siga

@app.get("/", tags=['Home'])
async def message():
    return HTMLResponse('<h1>¡Hello world!</h1>')

@app.get("/health", tags=['Health'])
async def health_check():
    """Endpoint para verificar el estado de la aplicación"""
    import os
    return JSONResponse(content={
        "status": "ok",
        "version": app.version,
        "database": "PostgreSQL" if os.getenv("PGHOST") else "SQLite",
        "db_initialized": _db_initialized
    }, status_code=200)

@app.post("/Login", tags=['auth'])
async def login(user: UserModel):
    token: str = create_token(user.model_dump())
    return JSONResponse(content={"token": token}, status_code=200)


@app.get("/debug/env", tags=['Debug'])
async def debug_env():
    import os
    return {
        "PGHOST": os.getenv("PGHOST", "NOT SET"),
        "PGPORT": os.getenv("PGPORT", "NOT SET"),
        "PGUSER": os.getenv("PGUSER", "NOT SET"),
        "PGDATABASE": os.getenv("PGDATABASE", "NOT SET"),
        "PGPASSWORD": "***" if os.getenv("PGPASSWORD") else "NOT SET"
    }

# Handler para Vercel
handler = app