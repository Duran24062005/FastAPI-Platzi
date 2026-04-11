import os
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

# Usar variable de entorno para la clave secreta
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "mi_llave_secreta_super_segura_cambiar_en_produccion")

def create_token(data: dict) -> str:
    """Crea un token JWT con los datos proporcionados"""
    token: str = encode(payload=data, key=SECRET_KEY, algorithm="HS256")
    return token

def decode_token(token: str) -> dict:
    """Decodifica y valida un token JWT"""
    try:
        data: dict = decode(token, SECRET_KEY, algorithms=['HS256'])
        return data
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")