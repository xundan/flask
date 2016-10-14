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
import time
from wxThread import WxThreadCollection, DemoThread
import json

app = Flask(__name__)
app.secret_key = '123'
ISO_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
WX_ID_NAME_DICT = {"cjkzy001": u"超级矿资源一圈",
                   "cjkzy003": u"超级矿资源三圈",
                   "cjkzy005": u"超级矿资源五圈",
                   "cjkzy007": u"超级矿资源煤炭交易平台",
                   "mgzdz456": u"超级矿资源非煤炭类交易平台",
                   "cjkzywl": u"超级矿资源物流信息平台",
                   "cjkzyshan": u"超级矿资源陕西物流",
                   "cjkzy012": u"超级矿资源山西物流",
                   "cjkzynmg": u"超级矿资源内蒙古物流",
                   "cjkzyhb": u"超级矿资源京津冀物流",
                   "cjkzyhn": u"超级矿资源河南物流",
                   "cjkzysd": u"超级矿资源山东物流",
                   "cjkzyjs": u"超级矿资源江苏安徽物流",
                   "cjkzyhh": u"超级矿资源湖南湖北物流",
                   "cjkzyxn": u"超级矿资源西南物流",
                   "cjkzyxb": u"超级矿资源西北物流",
                   "cjkzybgd": u"超级矿资源东北物流",
                   "cjkzynf": u"超级矿资源南方物流", }


@app.route('/')
def hello_world():
    return monitor()


@app.route('/monitor')
def monitor():
    wxs = []
    global THREAD_POOL, WX_ID_NAME_DICT
    for k in WX_ID_NAME_DICT.keys():
        living = "Dead"
        for td in THREAD_POOL.threads:
            if td.get_wx_id() == k:
                if td.is_stopped():
                    living = "Stopped"
                    break
                else:
                    living = "Alive"
                    break
        wx = Wx(k, WX_ID_NAME_DICT[k], living)
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
    print "url code: "+client_name
    if self_wx is not None and client_name is not None:
        record = Record(self_wx=self_wx, client_name=client_name)
    else:
        abort(404)
    return render_template('record_frame.html', record=record)


def send_record(self_wx, client_name, content):
    print "Now i am sending " + content + " from " + self_wx + " to " + client_name
    url = 'http://www.kuaimei56.com/index.php/Views/ChatRecord/record'
    params = {
        "self_wx": self_wx,
        "client_name": client_name,
        "content": content,
        "isme": 1,
        "type": "plain",
        "remark": "0"
    }
    post_server(url=url, params=params)


def delete_record(self_wx, client_name):
    #  todo set record invalid in sql
    print "Now I'm deleting " + self_wx + " to " + client_name
    pass
 

@app.route('/send', methods=['POST', ])
def send():
    """commit and show the record panel"""
    # record = None
    form = request.form
    self_wx = form.get('self_wx')
    client_name = form.get('client_name')
    content = form.get('content')
    if self_wx is None or client_name is None:
        abort(404)
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


@app.route('/kill_thread/<wx_id>')
def kill_thread(wx_id):
    global THREAD_POOL
    THREAD_POOL.kill(wx_id=wx_id)
    return monitor()


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
