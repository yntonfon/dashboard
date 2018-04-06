from sqlalchemy.exc import IntegrityError

from app.exception import UserAlreadyExistException
from app.mashaller import user_marshaller as user_marshaller_instance
from app.provider import security_provider as security_provider_instance
from app.repository import user_repository as user_repository_instance


class UserController:
    def __init__(self, user_repository, user_marshaller, security_provider):
        self.user_repository = user_repository
        self.user_marshaller = user_marshaller
        self.security_provider = security_provider
    
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


user_controller = UserController(user_repository_instance, user_marshaller_instance, security_provider_instance)
