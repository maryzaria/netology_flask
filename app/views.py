import pydantic
from flask import request, jsonify
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError

from schema import CreateAdvertisement, UpdateAdvertisement
from models import Advertisement, Session
from errors import HttpError
from main import app


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(response):
    request.session.close()
    return response


def validate(schema_class, json_data):
    try:
        return schema_class(**json_data).dict(exclude_unset=True)
    except pydantic.ValidationError as err:
        error = err.errors()[0]
        error.pop("ctx", None)
        raise HttpError(400, error)


def get_by_id(item_id):
    adv_item = request.session.get(Advertisement, item_id)
    if adv_item is None:
        raise HttpError(404, "Advertisement not found")
    return adv_item


def add_advertisement(adv):
    try:
        request.session.add(adv)
        request.session.commit()
    except IntegrityError:
        raise HttpError(409, "Advertisement already exists")


class AdvertisementView(MethodView):
    def get(self, advertisement_id):
        advertisement = get_by_id(advertisement_id)
        return jsonify(advertisement.dict)

    def post(self):
        json_data = validate(schema_class=CreateAdvertisement, json_data=request.json)
        new_adv = Advertisement(**json_data)
        add_advertisement(new_adv)
        return jsonify(new_adv.dict)

    def patch(self, advertisement_id):
        json_data = validate(json_data=request.json, schema_class=UpdateAdvertisement)
        advertisement = get_by_id(advertisement_id)
        for key, value in json_data.items():
            setattr(advertisement, key, value)
        add_advertisement(advertisement)
        return jsonify(advertisement.dict)

    def delete(self, advertisement_id):
        advertisement = get_by_id(advertisement_id)
        request.session.delete(advertisement)
        request.session.commit()
        return jsonify({"success": "Advertisement was deleted", "id": advertisement.id})
