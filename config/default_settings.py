import os


def get_int(var, default):
    return int(os.environ.get(var, default))


def get_bool(var, default):
    return bool(os.environ.get(var, default))


DEBUG = get_bool('DEBUG', False)

# API
API_URL_PREFIX = os.environ.get('API_URL_PREFIX', '/api')

# SECRET
SECRET_KEY = os.environ.get('SECRET_KEY', 'itsdangerous')

# URLSAFETIMED
URL_SAFE_TIMED_MAX_AGE = get_int('URL_SAFE_TIMED_MAX_AGE', 86400)

# SQLALCHEMY
SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI',
                                         "postgresql://invaders:Password01!@localhost/dashboard")
SQLALCHEMY_TRACK_MODIFICATIONS = get_bool('SQLALCHEMY_TRACK_MODIFICATIONS', False)

# BCRYPT
BCRYPT_LOG_ROUNDS = get_int('BCRYPT_LOG_ROUNDS', 12)

# MAIL
MAIL_SERVER = os.environ.get('MAIL_SERVER', 'localhost')
MAIL_PORT = get_int('MAIL_PORT', 8025)
MAIL_USE_TLS = get_bool('MAIL_USE_TLS', False)
MAIL_USE_SSL = get_bool('MAIL_USE_SSL', False)
MAIL_DEBUG = get_bool('MAIL_DEBUG', True)
MAIL_USERNAME = os.environ.get('MAIL_USERNAME', None)
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', None)
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', ("dashboard", "admin@test.com"))
MAIL_MAX_EMAILS = os.environ.get('MAIL_MAX_EMAILS', None)
MAIL_SUPPRESS_SEND = get_bool('MAIL_SUPPRESS_SEND', False)
MAIL_ASCII_ATTACHMENTS = get_bool('MAIL_ASCII_ATTACHMENTS', False)
