#!/usr/bin/env python
# coding: utf-8
import ConfigParser
import os
from flask import Flask
from flask import abort
from flask import render_template
from flask import request
from flask import url_for, flash
from models import Wx, ManualTodo, Record
import apiUtils
from newThread import WxThreadCollection, DemoThread
import json

ISO_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
WX_ID_NAME_DICT = {"cjkzy001": u"一圈",
                   "cjkzy003": u"三圈",
                   "cjkzy005": u"五圈",
                   "cjkzy007": u"煤炭交易平台",
                   "mgzdz456": u"非煤炭类交易平台",
                   "cjkzywl": u"物流信息平台",
                   "cjkzyshan": u"陕西",
                   "cjkzy012": u"山西",
                   "cjkzynmg": u"内蒙古",
                   "cjkzyhb": u"京津冀",
                   "cjkzyhn": u"河南",
                   "cjkzysd": u"山东",
                   "cjkzyjs": u"江苏安徽",
                   "cjkzyhh": u"湖南湖北",
                   "cjkzyxn": u"西南",
                   "cjkzyxb": u"西北",
                   "cjkzybgd": u"东北",
                   "cjkzynf": u"南方",
                   "cjkzy006": u"六圈",
                   "cjkzy008": u"八圈",
                   "cjkzy009": u"九圈",
                   "cjkzy010": u"十圈",
                   "cjkzy011": u"十一圈",
                   "cjkzysx": u"陕西",}
THREAD_POOL = None


def init_wxbot_dict():
    global THREAD_POOL
    THREAD_POOL = WxThreadCollection()

init_wxbot_dict()
app = Flask(__name__)
app.secret_key = '123'


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
    global THREAD_POOL
    for td in THREAD_POOL.threads:
        if td.is_stopped() is not True:
            manuals.append(td.get_wx_id())
    params = {
        "wx_list": manuals
    }
    print "params:" + json.dumps(params)
    dic = apiUtils.get_all_distinct_record(params=params)
    if dic["result_code"] != "201":
        print "is not 201"
        return render_template('manual_service.html', todos=[])
    else:
        print "right here!"
        result = dic["result"]
        todos = []
        for manual in result:
            todo = ManualTodo(manual["id"], manual['self_wx'], WX_ID_NAME_DICT[manual['self_wx']],
                              manual['client_name'], manual['record_time'], manual['status'])
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
        apiUtils.set_record_handled(self_wx, client_name)
        return render_template("record_frame.html", record=Record(self_wx, client_name))
    else:
        apiUtils.send_record(self_wx, client_name, content)
        return render_template("record_frame.html", record=Record(self_wx, client_name))


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
        thread = DemoThread(wx_id=wx_id)
        THREAD_POOL.add(thread)
        # time.sleep(2)
    png_path = url_for("static", filename="temp/wxqr.png")
    # png_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static/temp/wxqr.png")
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

if __name__ == '__main__':

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

