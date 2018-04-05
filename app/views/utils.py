from flask import jsonify


def handle_views_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
