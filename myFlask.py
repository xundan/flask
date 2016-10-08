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
from wxThread import WxThreadCollection, DemoThread

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


@app.route('/show/<id>')
def show(id):
    """commit and show the record panel"""
    thread = DemoThread(target_func=login_wx, s_args=(id,))
    global THREAD_POOL
    THREAD_POOL.add(thread)
    time.sleep(5)
    png_path = url_for("static", filename="temp/wxqr.png")
    print "They never come here." + png_path
    return render_template("qr_png.html", png_path=png_path)


@app.route('/show01')
def show_png01():
    # a_thread = threading.Thread(target=login_wx, args=('cjkzy001',))
    # a_thread.setDaemon(True)
    # a_thread.start()
    # sleep(2)
    thread = DemoThread(target_func=login_wx, s_args=('cjkzy001',))
    global THREAD_POOL
    THREAD_POOL.add(thread)
    time.sleep(5)
    png_path = url_for("static", filename="temp/wxqr.png")
    print "They never come here." + png_path
    return render_template("qr_png.html", png_path=png_path)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


# http://127.0.0.1:5000/query_user?id=3
def init_wxbot_dict():
    global THREAD_POOL
    THREAD_POOL = WxThreadCollection()

THREAD_POOL = None
if __name__ == '__main__':
    init_wxbot_dict()

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
