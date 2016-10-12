import json

import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from wxBot.testBot import MyWXBot

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Admin123@localhost/db'
db = SQLAlchemy(app)


class Wx(object):
    def __init__(self, wx_id, wx_name, wx_status):
        self.wx_id = wx_id
        self.wx_name = wx_name
        self.wx_status = wx_status


class ManualTodo(object):
    def __init__(self, todo_id, wx_id, wx_name, user_name, time, status):
        self.todo_id = todo_id
        self.wx_id = wx_id
        self.wx_name = wx_name
        self.user_name = user_name
        self.time = time
        self.status = status


class Record(object):
    def __init__(self, self_wx, client_name):
        self.self_wx = self_wx
        self.client_name = client_name
        self.content = self.fetch_content()

    def __repr__(self):
        return '<Record %r>' % self.content

    def fetch_content(self):
        url = "http://www.kuaimei56.com/index.php/Views/ChatRecord/distinct_record"
        params = {
            "self_wx": self.self_wx,
            "client_name": self.client_name
        }
        print "Record.getContent params:"+json.dumps(params)
        r = requests.post(url=url, json=params)
        print "Record.getContent return:"+MyWXBot.delete_bom(r.text)
        dic = json.loads(MyWXBot.delete_bom(r.text))
        if dic['result_code'] == '201':
            return dic['result']
        elif dic['reult_code'] == '202':
            return "No more message."
        else:
            return "Internal Error."
