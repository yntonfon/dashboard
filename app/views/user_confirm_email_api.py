from flask import jsonify, make_response
from flask.views import MethodView

from app.controller import user_controller
from app.exception import UserInvalidTokenException, ViewsException


class UserConfirmEmailAPI(MethodView):
    def get(self, token):
        try:
            user_controller.confirm_email(token)
        except UserInvalidTokenException as e:
            raise ViewsException(status_code=412, payload=e.messages)
        else:
            return make_response(jsonify(), 201)
