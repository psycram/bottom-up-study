from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./user.db'

db = SQLAlchemy(app)

app.config['SECRET_KEY'] = os.urandom(24)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "login"


from .models.models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


import webapp.views
