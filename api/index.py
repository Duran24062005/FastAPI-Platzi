import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from main import app

# Para Vercel, simplemente exportamos la app
# Vercel maneja automáticamente las aplicaciones ASGI
handler = app