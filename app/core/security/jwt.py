import os

from dotenv import load_dotenv
from fastapi import HTTPException
from jwt import ExpiredSignatureError, InvalidTokenError, decode, encode

load_dotenv()

SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "mi_llave_secreta_super_segura_cambiar_en_produccion",
)


def create_token(data: dict) -> str:
    return encode(payload=data, key=SECRET_KEY, algorithm="HS256")


def decode_token(token: str) -> dict:
    try:
        return decode(token, SECRET_KEY, algorithms=["HS256"])
    except ExpiredSignatureError as exc:
        raise HTTPException(status_code=401, detail="Token has expired") from exc
    except InvalidTokenError as exc:
        raise HTTPException(status_code=403, detail="Invalid token") from exc
