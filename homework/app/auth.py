import functools

from app import app
from errors import HttpError
from flask_bcrypt import Bcrypt
from models import MODEL, Token

from flask import request

bcrypt = Bcrypt(app)


def hash_password(password: str):
    """Функция для хеширования паролей"""
    password = password.encode()
    hashed = bcrypt.generate_password_hash(password)
    return hashed.decode()


def check_password(password: str, hashed_password: str):
    """Функция для проверки паролей"""
    password = password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.check_password_hash(password, hashed_password)


def check_owner(item: MODEL, user_id: int):
    """Проверка, является ли пользователь владельцем объявления"""
    if item.owner_id != user_id:
        raise HttpError(403, "Access denied")


def check_token(handler):
    """Декоратор для проверки токена пользователя"""

    @functools.wraps(handler)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Token")
        if token is None:
            raise HttpError(401, "Token not found")
        token = request.session.query(Token).filter_by(token=token).first()
        if token is None:
            raise HttpError(401, "Invalid token")
        request.token = token
        return handler(*args, **kwargs)

    return wrapper
