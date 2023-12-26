import pydantic
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError

from flask import Flask, jsonify, request
from flask.views import MethodView
from models import Session, User
from schema import CreateUser, UpdateUser

app = Flask("app")
# используем библиотеку для хеширования паролей
bcrypt = Bcrypt(app)


def hash_password(password: str):
    """Функция для хеширования паролей"""
    password = password.encode()
    hashed = bcrypt.generate_password_hash(password)
    return hashed.decode()  # преобразуем набор байтов в строку


def check_password(password: str, hashed_password: str):
    """Функция для проверки паролей"""
    password = password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.check_password_hash(password, hashed_password)


# def hello():
#     json_data = request.json
#     print(f"{json_data=}")
#     qs = request.args
#     print(f"qs: {qs}")
#     headers = request.headers
#     resp = jsonify({"hello": "world"})
#     return resp


def validate(schema_class, json_data):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except pydantic.ValidationError as err:
        error = err.errors()[0]
        error.pop("ctx", None)  # убираем поле контекста с технической информацией
        raise HttpError(400, error)


# flask позволяет прописать, что нужно сделать до запроса, а что после него
@app.before_request
def before_request():
    """Открыть сессию до запроса"""
    session = Session()
    request.session = session


@app.after_request
def after_request(response):
    """Открыть сессию после обработки запроса"""
    request.session.close()
    return response


class HttpError(Exception):
    def __init__(self, status_code: int, description: str):
        self.status_code = status_code
        self.description = description


# специальная функция для обработки исключений
@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({"error": error.description})
    response.status_code = error.status_code
    return response


def get_user_by_id(user_id: int):
    user = request.session.get(User, user_id)
    if user is None:
        raise HttpError(status_code=404, description="user not found")
    return user


def add_user(user: User):
    try:
        request.session.add(user)
        request.session.commit()
    except IntegrityError:
        raise HttpError(400, "user already exists")


class UserView(MethodView):
    def get(self, user_id):
        user = get_user_by_id(user_id)
        return jsonify(user.dict)

    def post(self):
        json_data = validate(CreateUser, request.json)
        json_data["password"] = hash_password(json_data["password"])
        # user = User(**request.json)
        user = User(**json_data)
        add_user(user)
        return jsonify(user.dict)

    def patch(self, user_id):
        json_data = validate(UpdateUser, request.json)
        if "password" in json_data:
            json_data["password"] = hash_password(json_data["password"])
        user = get_user_by_id(user_id)
        for key, value in json_data.items():
            setattr(user, key, value)
        add_user(user)
        return jsonify(user.dict)

    def delete(self, user_id):
        user = get_user_by_id(user_id)
        request.session.delete(user)
        request.session.commit()
        return jsonify(
            {
                "status": "deleted",
            }
        )


user_view = UserView.as_view("user")

# app.add_url_rule(
#     '/hello', view_func=hello, methods=["POST"],
# )

app.add_url_rule("/user", view_func=user_view, methods=["POST"])
app.add_url_rule(
    "/user/<int:user_id>", view_func=user_view, methods=["GET", "PATCH", "DELETE"]
)


if __name__ == "__main__":
    app.run()
