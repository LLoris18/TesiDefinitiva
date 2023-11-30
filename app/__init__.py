from flask import Flask
from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
mail = Mail(app)
from app import views
from app import admin_views
from app import models
from app.models import User
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
