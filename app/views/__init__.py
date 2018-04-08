from flask import Blueprint

from app.exception import ViewsException
from app.views.user_reset_password_api import UserResetPasswordAPI
from .user_confirm_email_api import UserConfirmEmailAPI
from .user_list_api import UserListAPI
from .utils import handle_views_exception

# Users API
user_blueprint = Blueprint('user', __name__)
user_blueprint.add_url_rule('/users', view_func=UserListAPI.as_view('users'))
user_blueprint.add_url_rule('/user/confirm/<string:token>', view_func=UserConfirmEmailAPI.as_view('user_confirm'))
user_blueprint.add_url_rule('/user/reset', view_func=UserResetPasswordAPI.as_view('user_reset'))
user_blueprint.register_error_handler(ViewsException, handle_views_exception)
