from flask import jsonify, request
from flask.views import MethodView
from marshmallow import ValidationError

from app.controller import user_controller, mail_controller
from app.exception import ViewsException, UserAlreadyExistException
from app.mashaller import user_marshaller
from app.validator import user_validator


class UserListAPI(MethodView):
    def get(self):
        users = user_controller.get_users()
        data = user_marshaller.serialize_list(users)
        return jsonify(data)
    
    def post(self):
        payload = request.get_json()
        try:
            user_validator.validate_create_payload(payload)
            data = user_controller.create_user(payload)
        except ValidationError as e:
            raise ViewsException(status_code=400, payload=e.messages)
        except UserAlreadyExistException as e:
            raise ViewsException(status_code=422, payload=e.messages)
        else:
            mail_controller.send_confirmation_email(payload['email'])
            return jsonify(data)
