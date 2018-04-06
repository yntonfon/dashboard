from app.exception import UserNotFoundException
from app.extension import sqlalchemy
from app.model import User


class UserRepository:
    @staticmethod
    def get_all():
        return User.query.all()
    
    @staticmethod
    def save(user):
        sqlalchemy.session.add(user)
        sqlalchemy.session.commit()
        return user.id

    @staticmethod
    def get_by(**kwargs):
        user = User.query.filter_by(**kwargs).first()
        if not user:
            raise UserNotFoundException()
        return user


user_repository = UserRepository
