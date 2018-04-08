from flask import request, jsonify, abort
from flask.views import MethodView

from app.controller import user_controller, mail_controller
from app.exception import UserNotFoundException, UserNotActiveException, ViewsException


class UserResetPasswordAPI(MethodView):
    def put(self):
        payload = request.get_json()
        email = payload['email']
    
        try:
            user = user_controller.get_user(email)
            user_controller.validate_user_status(user)
        except UserNotFoundException:
            abort(404)
        except UserNotActiveException as e:
            raise ViewsException(status_code=400, payload=e.messages)
    
        mail_controller.send_reset_password_link(email)
        return jsonify()
