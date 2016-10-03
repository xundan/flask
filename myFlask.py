#!/usr/bin/env python
# coding: utf-8
import ConfigParser
import os
from flask import Flask
from flask import abort
from flask import render_template
from flask import request
from flask import url_for, flash
from models import User, Wx, ManualTodo, Record
from wxBot.testBot import MyWXBot
import threading
import time
from time import ctime, sleep
from threadPool import ThreadPool

app = Flask(__name__)
app.secret_key = '123'
ISO_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


@app.route('/')
def hello_world():
    return monitor()


@app.route('/monitor')
def monitor():
    wxs = []
    for i in range(1, 11):
        wx = Wx('cjkzy' + str(i), 'cjkzy' + str(i), 'OK')
        wxs.append(wx)
    return render_template('monitor.html', wxs=wxs)


@app.route('/manual_service')
def manual_service():
    todos = []
    for i in range(1, 6):
        todo = ManualTodo(i, 'cjkzy' + str(i), 'cjkzy' + str(i), u'用户' + str(i),
                          time.strftime(ISO_TIME_FORMAT, time.localtime()), "On")
        todos.append(todo)
    return render_template('manual_service.html', todos=todos)


@app.route('/record_frame/<id>')
def record_frame(id):
    """show the record panel"""
    record = None
    if id == "On":
        record = Record(id)
    else:
        abort(404)
    return render_template('record_frame.html', record=record)


def send_record(record, content):
    #  todo send message by pushing content&record.client into get_bot(record.wx_id).queue
    print "Now i am sending "+content+" to "+record.client_name
    pass


def delete_record(record):
    #  todo set record invalid in sql
    print "Now I'm deleting "+record.id
    pass


@app.route('/send/<id>', methods=['POST', ])
def add(id):
    """commit and show the record panel"""
    record = None
    if id == "On":
        record = Record(id)
    else:
        abort(404)
    form = request.form
    content = form.get('content')
    if not content:
        flash("Manual deleted.")
        delete_record(record)
        return render_template("record_frame.html", record=record)
    else:
        send_record(record, content)
        return render_template("record_frame.html", record=record)


def login_wx(wx_id):
    print "now start wxbot by flask with: " + wx_id
    bot = MyWXBot(wx_id)
    bot.DEBUG = True
    bot.run()
    # png_path = url_for("static",filename="temp/wxqr.png")
    # print "They never come here."+png_path
    # return render_template("qr_png.html", png_path=png_path)


@app.route('/show01')
def show_png01():
    a_thread = threading.Thread(target=login_wx, args=('cjkzy001',))
    a_thread.setDaemon(True)
    a_thread.start()
    sleep(2)
    png_path = url_for("static", filename="temp/wxqr.png")
    print "They never come here." + png_path
    return render_template("qr_png.html", png_path=png_path)


@app.route('/show03')
def show_png03():
    a_thread = threading.Thread(target=login_wx, args=('cjkzy003',))
    a_thread.setDaemon(True)
    a_thread.start()
    sleep(2)
    png_path = url_for("static", filename="temp/wxqr.png")
    print "They never come here." + png_path
    return render_template("qr_png.html", png_path=png_path)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


# http://127.0.0.1:5000/query_user?id=3
def init_wxbot_dict():
    global THREAD_POOL
    THREAD_POOL = ThreadPool()
    THREAD_POOL.addTask("cjkzy001", login_wx, args=('cjkzy001',))
    THREAD_POOL.addTask("cjkzy003", login_wx, args=('cjkzy003',))


THREAD_POOL = None
if __name__ == '__main__':
    # a_thread = threading.Thread(target=init_wxbot_dict)
    # a_thread.setDaemon(True)
    # a_thread.start()
    # sleep(5)
    # THREAD_POOL.killTask("cjkzy001")
    # block the main thread

    # Get host info from 'host.ini'
    config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "host.ini")
    print ' * Now loading conf: ' + config_file_path
    localhost = '0.0.0.0'
    try:
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        localhost = cf.get('main', 'localhost')
    except Exception as e:
        print "[ERROR]Parse host.ini problem:"
        print e
    app.run(localhost)

    # print "Thread is appending here."
