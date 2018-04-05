from app.model import User, db


class UserRepository:
    @staticmethod
    def get_all():
        return User.query.all()
    
    @staticmethod
    def save(user):
        db.session.add(user)
        db.session.commit()
        return user.id


user_repository = UserRepository
