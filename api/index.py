#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Obtener el directorio raíz del proyecto
current_file = Path(__file__).resolve()
root_dir = current_file.parent.parent

# Agregar al path de Python
sys.path.insert(0, str(root_dir))

print(f"📁 Root directory: {root_dir}")
print(f"🐍 Python path: {sys.path}")

try:
    # Importar la aplicación
    from main import app
    
    print("✅ App importada exitosamente")
    
    # Vercel busca 'app' o 'application'
    application = app
    
    print(f"✅ Application exportada: {type(application)}")
    
except Exception as e:
    print(f"❌ Error al importar app: {e}")
    import traceback
    traceback.print_exc()
    raise