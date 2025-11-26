from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
from jwt_manager import create_token
from config.database import engine, Base
from middlewares.error import ErrorHandler
from router.user import UserModel
from router.user import user_router
from router.movie import movie_router
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
app.title = '⚙️Mi app con FastAPI🔧'
app.description = "🛠️My firstApp in FastAPI with Platzi🛠️"
app.version = '0.1.0'

app.add_middleware(ErrorHandler)

app.include_router(user_router)
app.include_router(movie_router)

# Variable para asegurar que solo se creen las tablas una vez
_tables_created = False

# Crear tablas en el primer request (no al importar el módulo)
@app.on_event("startup")
async def startup():
    global _tables_created
    if not _tables_created:
        try:
            logger.info("🔧 Creando tablas en la base de datos...")
            Base.metadata.create_all(bind=engine)
            logger.info("✅ Tablas creadas exitosamente")
            _tables_created = True
        except Exception as e:
            logger.error(f"❌ Error al crear tablas: {e}")
            raise

@app.get("/", tags=['Home'])
async def message():
    return HTMLResponse('<h1>¡Hello world!</h1>')

@app.get("/health", tags=['Health'])
async def health_check():
    """Endpoint para verificar el estado de la aplicación"""
    return JSONResponse(content={
        "status": "ok",
        "version": app.version,
        "tables_created": _tables_created
    }, status_code=200)

@app.post("/Login", tags=['auth'])
async def login(user: UserModel):
    token: str = create_token(user.model_dump())
    return JSONResponse(content={"token": token}, status_code=200)

# Handler para Vercel
handler = app