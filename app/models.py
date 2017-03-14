from . import db
import datetime

class User(db.Model):
    userid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    biography = db.Column(db.String(250), nullable=False)
    sex = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(80), nullable=False)
    profile_added_on = db.Column(db.DateTime, nullable=False)

    def __init__(self ,userid,first_name,last_name,username,sex,age,image,profile_added_on):
        self.userid=userid
        self.first_name = first_name
        self.last_name = last_name
        self.biography = biography
        self.sex = sex
        self.age = age
        self.image = image
        self.profile_added_on = profile_added_on

    def __repr__(self):
	    return '<User %r>' % self.username
