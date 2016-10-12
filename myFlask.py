#!/usr/bin/env python
# coding: utf-8
import ConfigParser
import os

import requests
from flask import Flask
from flask import abort
from flask import render_template
from flask import request
from flask import url_for, flash
from models import Wx, ManualTodo, Record
from wxBot.testBot import MyWXBot
from wxBot.wxbot import SafeSession
import time
from wxThread import WxThreadCollection, DemoThread
import json

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
    manuals = []
    url = "http://www.kuaimei56.com/index.php/Views/ChatRecord/all_distinct_record"
    global THREAD_POOL
    for td in THREAD_POOL.threads:
        if td.is_stopped() is not True:
            manuals.append(td.get_wx_id())
    params = {
        "wx_list": manuals
    }
    print "params:" + json.dumps(params)
    dic = post_server(url=url, params=params)
    if dic["result_code"] != "201":
        print "is not 201"
        return render_template('manual_service.html', todos=[])
    else:
        print "right here!"
        result = dic["result"]
        todos = []
        for manual in result:
            todo = ManualTodo(manual["id"], manual['self_wx'], manual['self_wx'], manual['client_name']
                              , manual['record_time'], manual['status'])
            todos.append(todo)
        return render_template('manual_service.html', todos=todos)


@app.route('/record_frame/<self_wx>/<client_name>')
def record_frame(self_wx, client_name):
    """show the record panel"""
    record = None
    if self_wx is not None and client_name is not None:
        record = Record(self_wx=self_wx, client_name=client_name)
    else:
        abort(404)
    return render_template('record_frame.html', record=record)


def send_record(self_wx, client_name, content):
    #  todo send message by pushing content&record.client into get_bot(record.wx_id).queue
    print "Now i am sending " + content + " from " + self_wx + " to " + client_name
    pass


def delete_record(self_wx, client_name):
    #  todo set record invalid in sql
    print "Now I'm deleting " + self_wx + " to " + client_name
    pass


@app.route('/send/<self_wx>/<client_name>', methods=['POST', ])
def add(self_wx, client_name):
    """commit and show the record panel"""
    # record = None
    if self_wx is None or client_name is None:
        abort(404)
    form = request.form
    content = form.get('content')
    if not content:
        flash("Manual deleted.")
        delete_record(self_wx, client_name)
        return render_template("record_frame.html", record=Record(self_wx, client_name))
    else:
        send_record(self_wx, client_name, content)
        return render_template("record_frame.html", record=Record(self_wx, client_name))


def login_wx(wx_id):
    print "now start wxbot by flask with: " + wx_id
    bot = MyWXBot(wx_id)
    bot.DEBUG = True
    bot.run()


@app.route('/show/<wx_id>')
def show(wx_id):
    """commit and show the record panel"""
    global THREAD_POOL
    is_exist = False
    for td in THREAD_POOL.threads:
        if td.get_wx_id() == wx_id and not td.is_stopped():
            is_exist = True
            break
    if not is_exist:
        thread = DemoThread(wx_id=wx_id, target_func=login_wx, s_args=(wx_id,))
        THREAD_POOL.add(thread)
        time.sleep(5)
    png_path = url_for("static", filename="temp/wxqr.png")
    # print "They never come here." + png_path
    return render_template("qr_png.html", png_path=png_path)


@app.route('/show01')
def show_png01():
    thread = DemoThread(wx_id='cjkzy001', target_func=login_wx, s_args=('cjkzy001',))
    global THREAD_POOL
    THREAD_POOL.add(thread)
    time.sleep(5)
    png_path = url_for("static", filename="temp/wxqr.png")
    print "They never come here." + png_path
    return render_template("qr_png.html", png_path=png_path)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


def post_server(url, params):
    r = requests.post(url, json=params)
    print "return:" + MyWXBot.delete_bom(r.text)
    return json.loads(MyWXBot.delete_bom(r.text))


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
