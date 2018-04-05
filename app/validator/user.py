from marshmallow import ValidationError

from app.schema import user_create_schema


class UserValidator:
    def __init__(self, user_create_schema):
        self.user_create_schema = user_create_schema
    
    def validate_create_payload(self, payload):
        errors = self.user_create_schema.validate(payload)
        if errors:
            raise ValidationError(errors)


user_validator = UserValidator(user_create_schema)
