from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from fastapi import HTTPException
 
my_key = 'mi_llave_secreta'

# def create_token(data: dict) -> str:
#     token: str = encode(payload=data, key=my_key, algorithm="HS256")
#     return token

# def decode_token(token: str) -> dict:
#     data: dict = decode(token, my_key, algorithms=['HS256'])
#     return data

# Función para crear el token
def create_token(data: dict) -> str:
    token: str = encode(payload=data, key=my_key, algorithm="HS256")
    return token

# Función para decodificar el token
def decode_token(token: str) -> dict:
    try:
        data: dict = decode(token, my_key, algorithms=['HS256'])
        return data
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except InvalidTokenError:
        raise HTTPException(status_code=403, detail="Invalid token")