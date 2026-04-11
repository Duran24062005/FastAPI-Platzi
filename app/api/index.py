#!/usr/bin/env python3
import sys
from pathlib import Path


current_file = Path(__file__).resolve()
root_dir = current_file.parent.parent.parent

if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from app.main import app

application = app
