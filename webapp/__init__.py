from flask import Flask
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

<<<<<<< HEAD
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
=======
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./user.db'
>>>>>>> develop

db = SQLAlchemy(app)

import webapp.views
