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
    
    # Register Bcrypt
    from app.provider import bcrypt
    bcrypt.init_app(app)
    
    # Register SQLAclchemy DB
    from app.model import db
    db.init_app(app)
    db.create_all(app=app)

    return app
