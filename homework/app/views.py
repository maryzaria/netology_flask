from auth import check_owner, check_password, check_token, hash_password
from errors import HttpError
from flask import jsonify, request
from flask.views import MethodView
from models import Advertisement, Session, Token, User
from schema import (
    CreateAdvertisement,
    CreateUser,
    Login,
    PatchUser,
    UpdateAdvertisement,
)
from tools import add_item, create_item, delete_item, get_by_id, update_item, validate

from app import app


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


class BaseView(MethodView):
    @property
    def token(self) -> Token:
        return request.token

    @property
    def user(self) -> User:
        return request.token.user


class UserView(BaseView):
    @check_token
    def get(self):
        return jsonify(self.user.dict)

    @staticmethod
    def post():
        payload = validate(CreateUser, request.json)
        payload["password"] = hash_password(payload["password"])
        user = create_item(User, payload)
        return jsonify(
            {
                "status": "success",
                "description": "User was registered",
                "id": user.id,
                "username": user.username,
            }
        )

    @check_token
    def patch(self):
        payload = validate(PatchUser, request.json)
        user = update_item(self.token.user, payload)
        return jsonify(
            {
                "status": "success",
                "description": "User's data were updated",
                "id": user.id,
                "username": user.username,
            }
        )

    @check_token
    def delete(self):
        user = self.token.user
        delete_item(user)
        return jsonify(
            {
                "status": "success",
                "description": "User's data were deleted",
                "id": user.id,
                "username": user.username,
            }
        )


class LoginView(BaseView):
    @staticmethod
    def post():
        payload = validate(Login, request.json)
        user = (
            request.session.query(User).filter_by(username=payload["username"]).first()
        )
        if user is None:
            raise HttpError(404, "User not found")
        if check_password(user.password, payload["password"]):
            token = create_item(Token, {"user_id": user.id})
            add_item(token)
            return jsonify({"token": token.token})
        raise HttpError(401, "Invalid password")


class AdvertisementView(BaseView):
    @check_token
    def get(self, adv_id: int = 0):
        if not adv_id:
            return jsonify(
                {"advertisements": [adv.dict for adv in self.user.advertisements]}
            )
        advertisement = get_by_id(adv_id, model=Advertisement)
        check_owner(advertisement, self.token.user_id)
        return jsonify(advertisement.dict)

    @check_token
    def post(self):
        json_data = validate(schema_class=CreateAdvertisement, json_data=request.json)
        json_data["owner_id"] = self.token.user_id
        # json_data["owner"] = self.user
        new_adv = Advertisement(**json_data)
        add_item(new_adv)
        return jsonify(new_adv.dict)

    @check_token
    def patch(self, adv_id: int):
        json_data = validate(json_data=request.json, schema_class=UpdateAdvertisement)
        advertisement = get_by_id(adv_id, model=Advertisement)
        check_owner(advertisement, self.token.user_id)
        update_item(advertisement, json_data)
        return jsonify(advertisement.dict)

    @check_token
    def delete(self, adv_id: int):
        advertisement = get_by_id(adv_id, model=Advertisement)
        check_owner(advertisement, self.token.user_id)
        delete_item(advertisement)
        return jsonify(
            {
                "status": "success",
                "description": "Advertisement was deleted",
            }
        )
