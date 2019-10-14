import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from findit.config import Config
from findit.models import Skill

skill_titles = ["C/C++", "C++", "C", "Python", "JavaScript", "Java", "Jopa"]

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def init_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from findit.users.routes import users
    from findit.vacancies.routes import vacancies
    from findit.main.routes import main
    from findit.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(vacancies)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    db_file = os.path.join(os.path.dirname(__file__), 'findit', 'storage.db')
    if not os.path.exists(db_file):
        with app.app_context():
            try:
                db.create_all()
                for title in skill_titles:
                    db.session.add(Skill(title))
            except:
                os.remove(db_file)
                print("Exception was thrown during database initialization. Interruption of app execution.")
                return None

    return app
