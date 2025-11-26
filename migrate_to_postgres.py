"""
Script para migrar datos iniciales a PostgreSQL
Ejecuta este script localmente antes de desplegar
"""
from config.database import Session, Base, engine
from model.movie_model import Movie, User2
from db import db_movie

# Crear todas las tablas
Base.metadata.create_all(bind=engine)

# Insertar películas de ejemplo
db = Session()

try:
    # Verificar si ya hay datos
    existing_movies = db.query(Movie).count()
    
    if existing_movies == 0:
        print("Insertando películas de ejemplo...")
        for movie_data in db_movie:
            movie = Movie(
                title=movie_data['title'],
                overview=movie_data['overview'],
                year=int(movie_data['year']),
                rating=float(movie_data['rating']),
                category=movie_data['category']
            )
            db.add(movie)
        
        db.commit()
        print(f"✅ {len(db_movie)} películas insertadas exitosamente")
    else:
        print(f"ℹ️ Ya existen {existing_movies} películas en la base de datos")
    
    # Crear usuario admin de ejemplo
    existing_users = db.query(User2).filter(User2.email == 'alexi@gmail.com').first()
    if not existing_users:
        print("Creando usuario administrador...")
        admin_user = User2(
            email='alexi@gmail.com',
            password='123456@JJ'  # En producción, usa hash de contraseñas
        )
        db.add(admin_user)
        db.commit()
        print("✅ Usuario admin creado")
    else:
        print("ℹ️ Usuario admin ya existe")
        
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()

print("\n🎉 Migración completada")