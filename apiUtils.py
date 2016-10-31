import json
import requests


def fetch_record_content(self_wx, client_name):
    """Get all chat record of this two person: self_wx & client_name."""
    url = "http://www.kuaimei56.com/index.php/Views/ChatRecord/distinct_record"
    params = {
        "self_wx": self_wx,
        "client_name": client_name
    }
    dic = post_server(url=url, params=params)
    if dic['result_code'] == '201':
        return dic['result']
    elif dic['result_code'] == '202':
        return "Self: No more message."
    else:
        return "Self: Internal Error."


def fetch_msg_to_send(wx_id):
    """Fetch wx_id's message to be sent."""
    url = 'http://www.kuaimei56.com/index.php/Views/ChatRecord/unsent_record'
    params = {
        "self_wx": wx_id
    }
    dic = post_server(url, params)

    if dic['result_code'] == '201':
        print '    fetch to be sent[Response]'
        print '    -----------------------------'
        print '    | to_send: %s' % dic['name']
        print '    | word: %s' % dic['word']
        print '    | result_code: %s' % dic['result_code']
        print '    | reason: %s' % dic['reason']
        print '    | error_code: %s' % dic['error_code']
        print '    -----------------------------'

        message = {"id": dic["message_id"], "name": dic["name"], "word": dic["word"]}
        return message
    elif dic['result_code'] == '202':
        return None
    print "[Error] [fetch_msg_to_send] DATABASE ERROR:" + dic['result_code']
    return None


def update_chat_msg_sent(record_id):
    """Mark the record as it had been sent."""
    url = 'http://www.kuaimei56.com/index.php/Views/ChatRecord/status'
    params = {
        "id": record_id,
        "status": 1
    }
    dic = post_server(url=url, params=params)
    print '    [Response]'
    print '    -----------------------------'
    print '    | result_code: %s' % dic['result_code']
    print '    | reason: %s' % dic['reason']
    print '    | error_code: %s' % dic['error_code']
    print '    | result: %s' % dic['result']
    print '    -----------------------------'
    return dic


def post_cjkzy_msg(wx_sender, msg_content, user_name):
    """Post this message to database raw-table."""
    url = 'http://www.kuaimei56.com/index.php/Views/Raw/messages'
    params = {
        "content": msg_content['data'],
        "sender": user_name,
        # "wx_sender": self.my_account['NickName']
        "wx_sender": wx_sender
    }
    dic = post_server(url=url, params=params)
    print '    [Response]'
    print '    -----------------------------'
    print '    | sender: %s' % user_name
    print '    | wx_sender: %s' % wx_sender
    print '    | result_code: %s' % dic['result_code']
    print '    | reason: %s' % dic['reason']
    print '    | error_code: %s' % dic['error_code']
    print '    | result: %s' % dic['result']
    print '    -----------------------------'
    return dic


def post_chat_record(wx_id, msg_content, user_name, isme=0, t_type="plain"):
    """Add chat record.
    If t_type is plain, this record need to be manual-handled.
    If t_type is msg, this is a classic message, which will process in auto-flow."""
    url = 'http://www.kuaimei56.com/index.php/Views/ChatRecord/record'
    params = {
        # "self_wx": self.wx_id,
        "self_wx": wx_id,
        "client_name": user_name,
        "content": msg_content['data'],
        "isme": isme,
        "type": t_type,
        "remark": "0"
    }
    dic = post_server(url=url, params=params)
    print '    [Response]'
    print '    -----------------------------'
    print '    | client_name: %s' % user_name
    print '    | self_wx: %s' % wx_id
    print '    | result_code: %s' % dic['result_code']
    print '    | reason: %s' % dic['reason']
    print '    | error_code: %s' % dic['error_code']
    print '    | result: %s' % dic['result']
    print '    -----------------------------'
    return dic


def send_record(self_wx, client_name, content):
    """Post the message-to-be-sent into database, """
    # print "Now i am sending " + content + " from " + self_wx + " to " + client_name
    url = 'http://www.kuaimei56.com/index.php/Views/ChatRecord/record'
    params = {
        "self_wx": self_wx,
        "client_name": client_name,
        "content": content,
        "isme": 1,
        "type": "plain",
        "remark": "0"
    }
    return post_server(url=url, params=params)


def get_all_distinct_record(params):
    """Get list of all distinct sessions to be manual-handled."""
    url = "http://www.kuaimei56.com/index.php/Views/ChatRecord/all_distinct_record"
    return post_server(url=url, params=params)


def post_server(url, params):
    r = requests.post(url, json=params)
    # print "return:" + delete_bom(r.text)
    return json.loads(delete_bom(r.text))


def delete_bom(text):
    """delete the BOM at head of text(json), if it has one."""
    if text is not None:
        while text[0] != "{":
            text = text[1:]
    return text
