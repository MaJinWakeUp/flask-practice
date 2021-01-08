# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 15:27:00 2020

@author: MaJin
"""
import os
from flask_sqlalchemy import SQLAlchemy
from flask import (Flask, render_template, make_response, 
                   redirect, abort, session, url_for, flash)
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_migrate import Migrate
from flask_mail import Mail
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from threading import Thread

basedir = os.path.abspath(os.path.dirname(__file__))

# chapter4
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

app=Flask(__name__)
# chapter4
app.config['SECRET_KEY'] = 'hard to guess string'
# chapter5
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# chapter6
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '[Flasky]'
app.config['FLASKY_MAIL_SENDER'] = 'Flasky Admin <flasky@example.com>'
app.config['FLASKY_ADMIN'] = os.environ.get('FLASKY_ADMIN')
mail = Mail(app)

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    # mail.send(msg)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr

# chapter5
db = SQLAlchemy(app)
# chapter3
bootstrap = Bootstrap(app)
moment = Moment(app)
migrate = Migrate(app, db)

# chapter5
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username

'''chapter3
@app.route('/')
def index():
    return render_template('index.html',
            current_time=datetime.utcnow())
'''
''' chapter4
@app.route('/', methods=['GET','POST'])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
    return render_template('index.html', form=form, 
            name=name, current_time=datetime.utcnow())

# with session and redirect
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form,
            name=session.get('name'))
'''

'''chapter5
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form,
            name=session.get('name'),known=session.get('known',False))

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)
'''
# chapter6
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if app.config['FLASKY_ADMIN']:
                send_email(app.config['FLASKY_ADMIN'], 'New User',
                            'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'),
                            known=session.get('known', False))

'''chapter2
@app.route('/user/<name>')
def get_user(name):
    if len(name)<2:
        abort(404)
    return '<h1>Hello, {}!</h1>'.format(name)
'''
# chapter3
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

# chapter3
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
'''
# chapter3
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
'''

# chapter2
@app.route('/bing')
def bing():
    return redirect('http://www.bing.com')

# chapter2
@app.route('/resp')
def resp():
    response = make_response('<h1>This document \
                             carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response

if __name__ == '__main__':
    app.run(debug=True) 
    # app.run(host='0.0.0.0', port=12346, debug=True, threaded = True) 