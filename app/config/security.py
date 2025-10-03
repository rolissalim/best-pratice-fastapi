from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from sqlalchemy.orm import joinedload, Session, load_only, selectinload
from app.models.user_model import UserToken, User
from fastapi.security import OAuth2PasswordBearer
from app.config.setting import get_settings
from app.config.database import get_session
import logging
import jwt
import base64

SPECIAL_CHARACTERS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>']

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/login")

def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def str_encode(string: str) -> str:
    return base64.b85encode(string.encode('ascii')).decode('ascii')


def str_decode(string: str) -> str:
    return base64.b85decode(string.encode('ascii')).decode('ascii')


def is_password_strong_enough(password: str) -> bool:
    if len(password) < 8:
        return False

    if not any(char.isupper() for char in password):
        return False

    if not any(char.islower() for char in password):
        return False

    if not any(char.isdigit() for char in password):
        return False

    if not any(char in SPECIAL_CHARACTERS for char in password):
        return False

    return True


def str_encode(string: str) -> str:
    return base64.b85encode(string.encode('ascii')).decode('ascii')


def str_decode(string: str) -> str:
    return base64.b85decode(string.encode('ascii')).decode('ascii')


def get_token_payload(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, settings.JWT_ALGORITHM)
    except Exception as jwt_exec:
        logging.debug(f"JWT Error: {str(jwt_exec)}")
        payload = None
    return payload


def create_access_token(payload: dict, expiry: timedelta):
    expire = datetime.now() + expiry
    payload.update({"exp": expire})
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)



async def get_token_user(token: str, db):
    payload = get_token_payload(token)
    if payload:
        user_token = db.query(UserToken).options(
            load_only(UserToken.user_id),
            joinedload(UserToken.user).load_only(User.id, User.name)
        ).filter(
            UserToken.access_key == payload.get('a'),
            UserToken.id == str_decode(payload.get('r')),
            UserToken.user_id == payload.get('user_id'),
            UserToken.expires_at > datetime.now()
        ).first()
        if user_token:
            return user_token, user_token.user
    return None, None


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    _, user = await get_token_user(token=token, db=db)
    if user:
        return user
    raise HTTPException(status_code=401, detail="Not authorized")
