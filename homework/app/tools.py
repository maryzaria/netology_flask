import pydantic
from flask import jsonify

from errors import HttpError
from app import app


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify(
        {"error": error.description}
    )
    response.status_code = error.status_code
    return response


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
