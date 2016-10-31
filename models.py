import apiUtils
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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
        self.content = apiUtils.fetch_record_content(self_wx, client_name)

    def __repr__(self):
        return '<Record %r>' % self.content

