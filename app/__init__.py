from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = "this is a super secure key"
app.config['SQLALCHEMY_DATABASE_URI'] = ": postgresql:/admin:Sweet#1@localhost/project1"
db = SQLAlchemy(app)
from app import views
from app.models import User


