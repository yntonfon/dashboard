from flask import Flask


def create_app(config=None):
    app = Flask(__name__)
    
    # Load the default configuration
    app.config.from_object('config.default_settings')

    if config:
        app.config.from_object(config)
    
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
    
    return app
