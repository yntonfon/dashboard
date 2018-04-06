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
        return User.query.filter_by(**kwargs).first()


user_repository = UserRepository
