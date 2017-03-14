"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""


import os
from flask import session,render_template, request, redirect, url_for, jsonify,flash
SECRET_KEY="super secure key"
from random import randint
from werkzeug.utils import secure_filename
from app.models import User
from sqlalchemy.sql import exists
from datetime import *
from app import app,db
import time
from form import ProfileForm
###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route('/profile/',methods=['GET','POST'])
def profile_add():
    form = ProfileForm(csrf_enabled=False)
    if request.method == 'POST':
        if form.validate_on_submit():
            username = request.form['username'].strip()
            first_name = request.form['first_name'].strip()
            last_name = request.form['last_name'].strip()
            sex = request.form['sex']
            age = request.form['age']
            biography = request.form['biography']
            image = request.files['image']
            while True:
                userid = randint(620000000,620099999)
                if not db.session.query(exists().where(User.userid == str(userid))).scalar():
                    break
            filename = secure_filename(image.filename)
            image.save(os.path.join('app/static/uploads', filename))
            profile_added_on = datetime.now()
            user = User(userid,first_name,last_name,username,sex,age,biography,filename,profile_added_on)
            db.session.add(user)
            db.session.commit()
            flash("User Successfully Added", category='success')
            return redirect('/profiles')
    return render_template('full_profile.html',form=form)

@app.route('/profile/<userid>', methods=['POST', 'GET'])
def selectedprofile(userid):
  user = User.query.filter_by(userid=userid).first()
  if not user:
      flash("Sorry Couldn't Find User" , category="danger")
  else:
      image = '/static/uploads/' + user.image
      if request.method == 'POST' and request.headers['Content-Type']== 'application/json':
            return jsonify(userid=user.userid, image=image,username=user.username, sex=user.sex, age=user.age, biography=user.biography, profile_added_on=user.profile_added_on)
      else:
            user = {'id':user.userid,'image':image, 'username':user.username,'first_name':user.first_name, 'last_name':user.last_name,'age':user.age, 'sex':user.sex, 'biography':user.biography,'profile_added_on':timeinfo(user.profile_added_on)}
            return render_template('profile.html', user=user)
  return redirect(url_for("profiles"))

def timeinfo(entry):
    day = time.strftime("%a")
    date = time.strftime("%d")
    if (date <10):
        date = date.lstrip('0')
    month = time.strftime("%b")
    year = time.strftime("%Y")
    return day + ", " + date + " " + month + " " + year

@app.route('/profiles', methods=["GET", "POST"])
def profiles():
  users = db.session.query(User).all()
  userlist=[]
  for user in users:
    userlist.append({'username':user.username,'userid':user.userid})
    if request.method == 'POST' and request.headers['Content-Type']== 'application/json':
        return jsonify(users=userlist)
  return render_template('profiles.html', users=users)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="5000")