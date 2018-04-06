from flask import Flask


def create_app(config_object=None):
    app = Flask(__name__, instance_relative_config=True)
    
    # Load the default configuration
    app.config.from_object('config.default')
    
    # Load the configuration from the instance folder
    app.config.from_pyfile('config.py')
    
    if config_object:
        app.config.from_object(config_object)
    else:
        # Load the file specified by the APP_CONFIG_FILE environment variable
        # Variables defined here will override those in the default configuration
        app.config.from_envvar('APP_CONFIG_FILE')
    
    # Register Blueprints
    from app.views import user_blueprint
    app.register_blueprint(user_blueprint, url_prefix=app.config['API_URL_PREFIX'])
    
    # Register Extensions
    from app.extension import bcrypt, mail, sqlalchemy
    bcrypt.init_app(app)
    mail.init_app(app)
    sqlalchemy.init_app(app)
    sqlalchemy.create_all(app=app)

    return app