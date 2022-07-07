from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # blueprint for testing
    from .Controller.Test_Route.Test import test2 as test2_blueprint
    app.register_blueprint(test2_blueprint)

    # blueprint for auth routes in our app
    from .Auth_Controller.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .Auth_Controller.app import app as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for testcode
    from .Controller.Testcode_Controller.Testcode_routes import tcc as test_blueprint
    app.register_blueprint(test_blueprint)

    # blueprint for calendar
    from .Controller.Calendar_Controller.Calendar_routes import cal as main_blueprint
    app.register_blueprint(main_blueprint)

     # blueprint for dashboard
    from .Controller.Dashboard_Controller.Dashboard_routes import dash as main_blueprint
    app.register_blueprint(main_blueprint)
    
     # blueprint for dashboard
    from .Controller.Eod_Controller.Eod_routes import eod as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .Controller.Mh_Controller.Mh_routes import mh as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .Controller.Tx_Controller.Tx_routes import tx as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .Controller.Figures_Controller.Figures_routes import fm as main_blueprint
    app.register_blueprint(main_blueprint)

    return app