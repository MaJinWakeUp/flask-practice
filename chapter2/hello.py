# -*- coding: utf-8 -*-
"""
Created on Mon Dec 21 15:27:00 2020

@author: MaJin
"""

from flask import Flask
from flask import make_response
from flask import redirect
from flask import abort

app=Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/bing')
def bing():
    return redirect('http://www.bing.com')

@app.route('/resp')
def resp():
    response = make_response('<h1>This document \
                             carries a cookie!</h1>')
    response.set_cookie('answer', '42')
    return response

@app.route('/user/<name>')
def get_user(name):
    if len(name)<2:
        abort(404)
    return '<h1>Hello, {}!</h1>'.format(name)

if __name__ == '__main__':
    app.run(debug=True) 
    # app.run(host='0.0.0.0', port=12346, debug=True, threaded = True) 