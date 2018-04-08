from flask import request, jsonify, abort, make_response
from flask.views import MethodView

from app.controller import user_controller, mail_controller
from app.exception import UserNotFoundException, UserNotActiveException, ViewsException, UserInvalidTokenException


class UserResetPasswordAPI(MethodView):
    def get(self):
        url_params = request.args
        
        try:
            result = user_controller.reset_password(url_params['token'])
        except UserInvalidTokenException:
            abort(404)
        else:
            mail_controller.send_new_password(**result)
            return make_response(jsonify(), 201)
    
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
        else:
            mail_controller.send_reset_password_link(email)
            return jsonify()
