from flask import request, jsonify
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from schema import CreateAdvertisement, UpdateAdvertisement
from tools import validate
from models import Advertisement, Session
from errors import HttpError
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


def get_by_id(item_id: int):
    adv_item = request.session.get(Advertisement, item_id)
    if adv_item is None:
        raise HttpError(404, "Advertisement not found")
    return adv_item


def add_advertisement(adv: Advertisement):
    try:
        request.session.add(adv)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "Advertisement already exists")


class AdvertisementView(MethodView):
    @staticmethod
    def get(adv_id: int):
        advertisement = get_by_id(adv_id)
        return jsonify(advertisement.dict)

    @staticmethod
    def post():
        json_data = validate(schema_class=CreateAdvertisement, json_data=request.json)
        new_adv = Advertisement(**json_data)
        add_advertisement(new_adv)
        return jsonify(new_adv.dict)

    @staticmethod
    def patch(adv_id: int):
        json_data = validate(json_data=request.json, schema_class=UpdateAdvertisement)
        advertisement = get_by_id(adv_id)
        for key, value in json_data.items():
            setattr(advertisement, key, value)
        add_advertisement(advertisement)
        return jsonify(advertisement.dict)

    @staticmethod
    def delete(adv_id: int):
        advertisement = get_by_id(adv_id)
        request.session.delete(advertisement)
        request.session.commit()
        return jsonify({
             "status": "success",
             "description": "Advertisement was deleted",
        })


