#!/usr/bin/env python3
import sys
from pathlib import Path

current_file = Path(__file__).resolve()
root_dir = current_file.parent.parent.parent

sys.path.insert(0, str(root_dir))

print(f"📁 Root directory: {root_dir}")
print(f"🐍 Python path: {sys.path}")

try:
    from app.main import app
    
    print("✅ App importada exitosamente")
    
    application = app
    
    print(f"✅ Application exportada: {type(application)}")
    
except Exception as e:
    print(f"❌ Error al importar app: {e}")
    import traceback
    traceback.print_exc()
    raise
