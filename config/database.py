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

# Construcción de la URL de PostgreSQL
DB_USER = os.getenv("PGUSER", "postgres")
DB_PASSWORD = os.getenv("PGPASSWORD", "")
DB_HOST = os.getenv("PGHOST", "localhost")
DB_PORT = os.getenv("PGPORT", "5432")
DB_NAME = os.getenv("PGDATABASE", "movies_db")

# URL de conexión PostgreSQL
database_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Para desarrollo local con SQLite (opcional)
# database_url = "sqlite:///./database.sqlite"

engine = create_engine(
    database_url,
    echo=True,
    pool_pre_ping=True,  # Verifica conexiones antes de usarlas
    pool_recycle=3600,   # Recicla conexiones cada hora
)

Session = sessionmaker(bind=engine)

Base = declarative_base()
