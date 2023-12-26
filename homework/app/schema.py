from abc import ABC

import pydantic
from typing import Optional


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
    owner: str

    @pydantic.field_validator("owner")
    @classmethod
    def check_owner(cls, value: str):
        if len(value) > 50:
            raise ValueError("Owner's name must be less than 50 chars")
        return value


class UpdateAdvertisement(AbstractAdv):
    title: Optional[str] = None
    description: Optional[str] = None

