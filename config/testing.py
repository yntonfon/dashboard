TESTING = True

# SQLALCHEMY
SQLALCHEMY_DATABASE_URI = "postgresql://invaders:Password01!@localhost/test-dashboard"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# BCRYPT
BCRYPT_LOG_ROUNDS = 12

# MAIL
MAIL_DEBUG = True
MAIL_DEFAULT_SENDER = ('root', 'localhost@test.com')
MAIL_SUPPRESS_SEND = True
