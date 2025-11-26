# import os
# from sqlalchemy import create_engine
# from sqlalchemy.orm.session import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

# sqlite_file_name = "../database.sqlite"
# base_dir = os.path.dirname(os.path.realpath(__file__))

# database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

# engine = create_engine(database_url, echo=True)

# Session = sessionmaker(bind=engine)

# Base = declarative_base()




import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

# Obtener variables de entorno
DB_USER = os.getenv("PGUSER")
DB_PASSWORD = os.getenv("PGPASSWORD")
DB_HOST = os.getenv("PGHOST")
DB_PORT = os.getenv("PGPORT", "5432")
DB_NAME = os.getenv("PGDATABASE")

# Verificar si están configuradas las variables de PostgreSQL
if all([DB_USER, DB_PASSWORD, DB_HOST, DB_NAME]):
    # Usar PostgreSQL
    database_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    print(f"🐘 Conectando a PostgreSQL en {DB_HOST}")
else:
    # Fallback a SQLite solo para desarrollo local
    print("⚠️ Variables de PostgreSQL no encontradas, usando SQLite")
    database_url = "sqlite:///./database.sqlite"

print(f"📊 Database URL: {database_url.split('@')[0]}@****")  # Log sin mostrar contraseña

engine = create_engine(
    database_url,
    echo=False,  # Cambiar a False en producción para menos logs
    pool_pre_ping=True,  # Verifica conexiones antes de usarlas
    pool_recycle=3600,   # Recicla conexiones cada hora
    connect_args={"sslmode": "require"} if "postgresql" in database_url else {}
)

Session = sessionmaker(bind=engine)

Base = declarative_base()
