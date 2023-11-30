from . import app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy(app)
from app.__init__ import login_manager
from datetime import datetime
class User(UserMixin, db.Model):
    __tablename__ = 'utenti'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(256))
    confirmed = db.Column(db.Boolean, default=False, nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


'''
with app.app_context():
    db.drop_all()
    db.create_all()
'''