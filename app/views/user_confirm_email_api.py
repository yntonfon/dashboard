from flask.views import MethodView


class UserConfirmEmailAPI(MethodView):
    def get(self, token):
        pass
