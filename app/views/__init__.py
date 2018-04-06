from flask import Blueprint

from app.exception import ViewsException
from .user_list_api import UserListAPI
from .utils import handle_views_exception

# Users API
user_blueprint = Blueprint('user', __name__)
user_blueprint.add_url_rule('/users', view_func=UserListAPI.as_view('users'))
user_blueprint.register_error_handler(ViewsException, handle_views_exception)
