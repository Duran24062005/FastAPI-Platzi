import os

from dotenv import load_dotenv

load_dotenv()

app_config = {
    "APP_NAME": "Mi app con FastAPI",
    "VERSION": "0.2.0",
    "DESCRIPTION": "API organizada por capas con repository pattern",
    "HOST": os.getenv("HOST", "0.0.0.0"),
    "PORT": int(os.getenv("PORT", "8000")),
}
