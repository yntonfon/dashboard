from itsdangerous import BadData
from sqlalchemy.exc import IntegrityError

from app.exception import UserAlreadyExistException, UserInvalidTokenException, UserNotFoundException
from app.mashaller import user_marshaller as user_marshaller_instance
from app.provider import security_provider as security_provider_instance, SaltEnum
from app.repository import user_repository as user_repository_instance


class UserController:
    def __init__(self, user_repository, user_marshaller, security_provider):
        self.user_repository = user_repository
        self.user_marshaller = user_marshaller
        self.security_provider = security_provider
        self.app = None

    def init_app(self, app):
        self.app = app
    
    def get_users(self):
        return self.user_repository.get_all()
    
    def create_user(self, payload):
        user = self.user_marshaller.deserialize(payload)
        user.password_hash = self.security_provider.encrypt_password(payload['password'])
        try:
            user_id = self.user_repository.save(user)
        except IntegrityError:
            raise UserAlreadyExistException()
        else:
            return {'id': user_id}

    def confirm_email(self, token):
        try:
            email = self.security_provider.decrypt_from_urlsafetimed(token, salt=SaltEnum.email_confirmation.value)
            user = self.user_repository.get_by(email=email)
        except (BadData, UserNotFoundException):
            raise UserInvalidTokenException()
        else:
            user.email_confirmed = True
            return self.user_repository.save(user)


user_controller = UserController(user_repository_instance,
                                 user_marshaller_instance,
                                 security_provider_instance)
