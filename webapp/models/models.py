from webapp import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255))

class Curriculum(db.Model):
    id = db.Column(db.Integer, primary_key=True)
<<<<<<< HEAD
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
    
=======
    subject = db.Column(db.String(255), nullable=False)
    level = db.Column(db.String(255), nullable=False)
    unit = db.Column(db.String(255),nullable=False)
    course = db.Column(db.String(255),nullable=False)
    
    from flask_sqlalchemy import SQLAlchemy

# 科目（Subject）
class Subject(db.Model):
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    levels = db.relationship('Level', backref='subject', lazy=True)

# レベル（Level）
class Level(db.Model):
    __tablename__ = 'levels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    units = db.relationship('Unit', backref='level', lazy=True)

# 単元（Unit）
class Unit(db.Model):
    __tablename__ = 'units'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'), nullable=False)
    courses = db.relationship('Course', backref='unit', lazy=True)

# 講座（Course）
class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    unit_id = db.Column(db.Integer, db.ForeignKey('units.id'), nullable=False)
    lectures = db.relationship('Lecture', backref='course', lazy=True)
    
# 講座（Course）
class Lecture(db.Model):
    __tablename__ = 'lectures'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    file = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(100), nullable=False)
    options = db.relationship('Option', backref='lecture', lazy=True)

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)

class Option(db.Model):
    __tablename__ = 'options'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False, default=False)

    lecture_id = db.Column(db.Integer, db.ForeignKey('lectures.id'), nullable=False)
>>>>>>> develop
