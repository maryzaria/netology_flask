from flask import jsonify

from main import app


class HttpError(Exception):
    def __init__(self, status_code, description):
        self.status_code = status_code
        self.description = description


@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify(
        {"error": error.description}
    )
    response.status_code = error.status_code
    return response
