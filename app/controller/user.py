from sqlalchemy.exc import IntegrityError

from app.exception.user import UserAlreadyExistException
from app.mashaller import user_marshaller
from app.provider import security
from app.repository import user_repository


class UserController:
    def __init__(self, user_repository, user_marshaller, security):
        self.user_repository = user_repository
        self.user_marshaller = user_marshaller
        self.security = security
    
    def get_users(self):
        return self.user_repository.get_all()
    
    def create_user(self, payload):
        user = self.user_marshaller.deserialize(payload)
        user.password_hash = self.security.encrypt_password(payload['password'])
        try:
            user_id = self.user_repository.save(user)
        except IntegrityError:
            raise UserAlreadyExistException()
        else:
            return {'id': user_id}


user_controller = UserController(user_repository, user_marshaller, security)
