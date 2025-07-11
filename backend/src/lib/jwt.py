from authlib.jose import jwt, JoseError
from fastapi import HTTPException
from dotenv import load_dotenv
from time import time
import os


load_dotenv
JWT_KEY = os.getenv('JWT_KEY')
ALGORITHM = 'HS256'
TOKEN_EXPIRE_SECONDS = 7 * 24 * 60 * 60 #7 days


def create_token(data: dict):
    payload = data
    payload.update({
        'exp':time() + TOKEN_EXPIRE_SECONDS,
        'iat':time()
    })
    token = jwt.encode({'alg': ALGORITHM}, payload, JWT_KEY).decode('utf-8')
    return token

    
def verify_token(token: str):
    if not token:
        raise HTTPException(401,'Unauthorized - No token found')
    try:
        payload = jwt.decode(token, JWT_KEY)
        return payload
    except JoseError:
        print(JoseError)
        raise HTTPException(401,'Unauthorized - Invalid token')