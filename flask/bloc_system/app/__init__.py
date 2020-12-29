from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Flask
from flask_bootstrap import Bootstrap
db = SQLAlchemy()
bootstrap = Bootstrap()
login_mangeer = LoginManager()
login_mangeer.session_protection = 'strong'
login_mangeer.login_view = 'auth.login'

from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    bootstrap.init_app(app)

    from .auth import auth

    app.register_blueprint(auth,url_prefix='/auth')
    login_mangeer.init_app(app)
    from .main import main
    app.register_blueprint(main)

    db.init_app(app)
    return app