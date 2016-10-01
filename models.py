from sqlalchemy import Column, Integer, String, TIMESTAMP, TEXT, func
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Admin123@localhost/db'
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.name


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


class Record(db.Model):
    __tablename__ = 'records'
    id = Column(Integer, primary_key=True)
    self_wx = Column(String(50), unique=False)
    client_name = Column(String(200), unique=False)
    content = Column(TEXT, unique=False)
    is_me = Column(Integer, unique=False)
    type = Column(String(50), unique=False)
    remark = Column(String(100), unique=False)
    record_time = Column(TIMESTAMP, server_default=func.now())
    status = Column(Integer, unique=False)
    invalid_id = Column(Integer, unique=False)

    def __init__(self, id):
        self.id = id
        self.content = "would be select from db later"

    def __repr__(self):
        return '<Record %r>' % self.content

