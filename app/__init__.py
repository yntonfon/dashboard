import os

from flask import Flask

from config.logger import init_logger


def create_app(config=None):
    app = Flask(__name__)
    
    # Load the default configuration
    app.config.from_object('config.default_settings')

    if config:
        app.config.from_object(config)

    if os.environ.get('APP_CONFIG_FILE'):
        # Load the file specified by the APP_CONFIG_FILE environment variable
        # Variables defined here will override those in the default configuration
        app.config.from_envvar('APP_CONFIG_FILE')
    
    return app


def bootstrap_app(app=None, config=None):
    if not app:
        app = create_app(config)
    elif config:
        app.config.update(config)
    
    # Register Blueprints
    from app.views import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix=app.config['API_URL_PREFIX'])
    
    # Register Extensions
    from app.extension import bcrypt, mail, sqlalchemy
    bcrypt.init_app(app)
    mail.init_app(app)
    sqlalchemy.init_app(app)
    sqlalchemy.create_all(app=app)
    
    # Register Provider
    from app.provider import security_provider
    security_provider.init_app(app)

    # Init logger
    init_logger(app, app.logger)
    
    return app
