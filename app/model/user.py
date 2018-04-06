from app.extension import sqlalchemy


class User(sqlalchemy.Model):
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String(64), unique=True, index=True)
    email = sqlalchemy.Column(sqlalchemy.String(120), unique=True, index=True)
    password_hash = sqlalchemy.Column(sqlalchemy.String(128), nullable=False)
    email_confirmed = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
