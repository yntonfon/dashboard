from app.schema import user_schema


class UserMarshaller:
    def __init__(self, user_schema):
        self.user_schema = user_schema
    
    def deserialize(self, payload):
        user, _ = self.user_schema.load(payload)
        return user
    
    def serialize(self, user, many=False):
        return self.user_schema.dump(user, many=many).data
    
    def serialize_list(self, users):
        return self.serialize(users, many=True)


user_marshaller = UserMarshaller(user_schema)
