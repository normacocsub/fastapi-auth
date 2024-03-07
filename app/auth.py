import os

import jwt
from datetime import timedelta, datetime
from typing import Optional
from dotenv import load_dotenv
from fastapi.security import HTTPAuthorizationCredentials

import bcrypt

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = 30
SECRET_KEY = os.getenv('SECRET_TOKEN')
ALGORITHM = 'HS256'


def encrypt_password(password: str):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')


def equals_password(password: str, hashed_password: str):
    password_bytes = password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_password_bytes)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: HTTPAuthorizationCredentials):
    try:
        return jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception as e:
        print(e)
        return False
