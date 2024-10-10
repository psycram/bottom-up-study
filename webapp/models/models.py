from webapp import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255))

class Curriculum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    goallevel = db.Column(db.Integer, nullable=False)
    startlevel = db.Column(db.Integer,nullable=False)
    content4 = db.Column(db.String(255))
    content5 = db.Column(db.String(255))
    content6 = db.Column(db.String(255))
    content7 = db.Column(db.String(255))
    content8 = db.Column(db.String(255))
    content9 = db.Column(db.String(255))
    content10 = db.Column(db.String(255))
    content11 = db.Column(db.String(255))
    content12 = db.Column(db.String(255))
    content1 = db.Column(db.String(255))
    content2 = db.Column(db.String(255))
    