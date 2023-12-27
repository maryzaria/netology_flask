import psycopg2
import pydantic
from errors import HttpError
from flask import jsonify, request
from models import MODEL, MODEL_TYPE
from sqlalchemy.exc import IntegrityError

from app import app


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.description})
    response.status_code = error.status_code
    return response


@app.errorhandler(500)
def unexpected(err):
    msg = {"description": "unexpected error"}
    if app.debug:
        msg["error"] = str(err)
        msg["traceback"] = err.__traceback__
    return get_json_response(msg, 500)


def get_json_response(json_data: dict, status_code: int = 200):
    response = jsonify(json_data)
    response.status_code = status_code
    return response


def validate(schema_class, json_data: dict):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except pydantic.ValidationError as err:
        error = err.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)


def get_by_id(item_id: int, model: MODEL_TYPE) -> MODEL:
    adv_item = request.session.get(model, item_id)
    if adv_item is None:
        raise HttpError(404, f"{model.__name__} not found")
    return adv_item


# def add_advertisement(adv: Advertisement):
#     try:
#         request.session.add(adv)
#         request.session.commit()
#     except IntegrityError:
#         raise HttpError(409, "Advertisement already exists")


def add_item(item: MODEL) -> MODEL:
    try:
        request.session.add(item)
        request.session.commit()
    except IntegrityError as err:
        if isinstance(err.orig, psycopg2.errors.UniqueViolation):
            raise HttpError(409, f"{item.__class__.__name__} already exists")
        else:
            raise err
    return item


def create_item(model: MODEL_TYPE, payload: dict) -> MODEL:
    item = model(**payload)
    item = add_item(item)
    return item


def delete_item(item: MODEL):
    request.session.delete(item)
    request.session.commit()


def update_item(item: MODEL, payload: dict) -> MODEL:
    for field, value in payload.items():
        setattr(item, field, value)
    add_item(item)
    return item
