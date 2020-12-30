# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 15:27:00 2020

@author: MaJin
"""

from flask import (Flask, render_template, make_response, 
                   redirect, abort, session, url_for)
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# chapter4
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

app=Flask(__name__)
# chapter4
app.config['SECRET_KEY'] = 'hard to guess string'
# chapter3
bootstrap = Bootstrap(app)
moment = Moment(app)

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
'''
# with session and redirect
@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form,
            name=session.get('name'))

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