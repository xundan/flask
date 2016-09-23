#!/usr/bin/env python
# coding: utf-8
import ConfigParser
import os
from flask import Flask
from flask import abort
from flask import render_template
from flask import request
from flask import url_for, flash
from models import User
from wxBot.testBot import MyWXBot

app = Flask(__name__)
app.secret_key = '123'


@app.route('/')
def hello_world():
    content = 'Hello content!'
    flash('hello flash')
    return render_template('index.html', content=content)


@app.route('/login', methods=['POST'])
def login():
    form = request.form
    user_name = form.get('user_name')
    password = form.get('password')
    if not user_name:
        flash("Please input your name.")
        return render_template("index.html", content='nothing')
    if not password:
        flash("Please input your password.")
        return render_template("index.html", content='nothing')

    if user_name == 'xcl' and password == 'xcl':
        flash("Login successfully.")
        return render_template("son2_base.html")
    else:
        flash("Login failed")
        return render_template("index.html", content='nothing')


@app.route('/login01')
def login01():
    # print "now start wxbot by flask"
    # bot = MyWXBot()
    # bot.DEBUG = True
    # bot.run()
    png_path = url_for("static",filename="temp/wxqr.png")
    print "They never come here."+png_path
    return render_template("qr_png.html", png_path=png_path)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@app.route('/user')
def show_user():
    user = User(123, 'xcl')
    return render_template('user.html', user=user)


@app.route('/user/<id>')
def user_id(id):
    user = None
    if int(id) == 1:
        user = User(1, 'xuncl')
    else:
        abort(404)
    return render_template('user_id.html', user=user)


@app.route('/users')
def users():
    users = []
    for i in range(1, 11):
        user = User(i, 'xcl' + str(i))
        users.append(user)
    return render_template('users.html', users=users)


@app.route('/one')
def one():
    return render_template('son_base.html')


@app.route('/two')
def two():
    return render_template('son2_base.html')


@app.route('/user', methods=['POST'])
def hello_user():
    return 'Hello user'


@app.route('/query_user')
def query_id():
    id = request.args.get('id')
    return 'Hello ' + id


# http://127.0.0.1:5000/query_user?id=3


@app.route('/query_url')
def query_url():
    return 'query url:' + url_for('query_id')


if __name__ == '__main__':
    config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "host.ini")
    print ' * Now loading conf: '+config_file_path
    localhost = '0.0.0.0'
    try:
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        localhost = cf.get('main', 'localhost')
    except Exception as e:
        print "[ERROR]Parse host.ini problem:"
        print e
    app.run(localhost)
