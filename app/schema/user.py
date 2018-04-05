from marshmallow import fields, Schema, post_load, validate

from app.model import User


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    email = fields.Email()
    email_confirmed = fields.Boolean(dump_only=True)
    password_hash = fields.Str(load_only=True, dump_only=True)
    
    @post_load
    def make_user(self, data):
        return User(**data)


class UserCreateSchema(Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=1))


user_schema = UserSchema()
user_create_schema = UserCreateSchema()
