class UserDomain:
    def is_active(self, user):
        return user.email_confirmed


user_domain = UserDomain()
