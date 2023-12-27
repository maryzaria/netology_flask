import re
from abc import ABC
from typing import Optional

import pydantic
from flask import request
from models import User


class AbstractUser(pydantic.BaseModel, ABC):
    username: str
    password: str
    email: Optional[str]


class Login(AbstractUser):
    pass


class PatchUser(AbstractUser):
    name: Optional[str] = None
    password: Optional[str] = None

    @pydantic.field_validator("username")
    @classmethod
    def check_username(cls, username: str) -> str:
        user = request.session.query(User).filter_by(username=username).first()
        if user:
            raise ValueError("Username already exists")
        if len(username) > 50:
            raise ValueError("Username must be less than 50 symbols")
        return username

    @pydantic.field_validator("password")
    @classmethod
    def secure_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Minimal length of password is 8")
        if len(v) > 32:
            raise ValueError("Maxima length of password is 32")
        return v


class CreateUser(PatchUser):
    @pydantic.field_validator("email")
    @classmethod
    def check_email(cls, email: str) -> str:
        user_email = request.session.query(User).filter_by(email=email).first()
        if user_email:
            raise ValueError("Email address already exists. Try to login")
        if len(email) > 50:
            raise ValueError("Maxima length of email address is 50")
        if not re.search(r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{2,})", email):
            raise ValueError(
                "Email address doesn't fit the format, example: example@mail.com"
            )
        return email


class AbstractAdv(pydantic.BaseModel, ABC):
    title: Optional[str]
    description: Optional[str]

    @pydantic.field_validator("title")
    @classmethod
    def check_ad_header(cls, value: str):
        if len(value) > 100:
            raise ValueError("Title must be less than 100 chars")
        return value

    @pydantic.field_validator("description")
    @classmethod
    def check_description(cls, value: str):
        if len(value) > 200:
            raise ValueError("Description must be less than 200 chars")
        return value


class CreateAdvertisement(AbstractAdv):
    title: str
    description: str


class UpdateAdvertisement(AbstractAdv):
    title: Optional[str] = None
    description: Optional[str] = None
