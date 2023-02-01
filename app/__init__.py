from flask import Flask
from flask_bootstrap import Bootstrap
from app.config import ProdConfig
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_admin import Admin


db = SQLAlchemy()
migrate = Migrate()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = "account.login"
login_manager.login_message = "Please login to access this page."
mail = Mail()
admin = Admin()



def create_app(config=ProdConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app.admin_bp import AdminIndex

    admin.init_app(app, index_view=AdminIndex())
    
    from .product import bp as main_bp
    app.register_blueprint(main_bp)

    from .account import bp as account_bp
    app.register_blueprint(account_bp)

    from .errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from .order import bp as order_bp
    app.register_blueprint(order_bp)

    from .admin_bp import bp as admin_bp
    app.register_blueprint(admin_bp)

    return app


#from app import models

