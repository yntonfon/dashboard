from flask import request, jsonify, abort
from flask.views import MethodView

from app.controller import user_controller, mail_controller
from app.exception import UserNotFoundException


class UserResetPasswordAPI(MethodView):
    def put(self):
        payload = request.get_json()
        email = payload['email']
    
        try:
            user_controller.get_user(email)
        except UserNotFoundException:
            abort(404)
    
        mail_controller.send_reset_password_link(email)
        return jsonify()
