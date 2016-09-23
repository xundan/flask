#!/usr/bin/env python
# coding: utf-8

from wxbot import *
import ConfigParser
import json


class TulingWXBot(WXBot):
    def __init__(self):
        WXBot.__init__(self)

        self.tuling_key = ""
        self.robot_switch = True

        try:
            cf = ConfigParser.ConfigParser()
            cf.read('conf.ini')
            self.tuling_key = cf.get('main', 'key')
        except Exception:
            pass
        print 'tuling_key:', self.tuling_key

    def tuling_auto_reply(self, uid, msg):
        if self.tuling_key:
            url = "http://www.tuling123.com/openapi/api"
            user_id = uid.replace('@', '')[:30]
            body = {'key': self.tuling_key, 'info': msg.encode('utf8'), 'userid': user_id}
            r = requests.post(url, data=body)
            respond = json.loads(r.text)
            result = ''
            if respond['code'] == 100000:
                result = respond['text'].replace('<br>', '  ')
            elif respond['code'] == 200000:
                result = respond['url']
            elif respond['code'] == 302000:
                for k in respond['list']:
                    result = result + u"【" + k['source'] + u"】 " + \
                             k['article'] + "\t" + k['detailurl'] + "\n"
            else:
                result = respond['text'].replace('<br>', '  ')

            print '    ROBOT:', result
            return result
        else:
            return u"知道啦"

    def auto_switch(self, msg):
        msg_data = msg['content']['data']
        stop_cmd = [u'退下', u'走开', u'关闭', u'关掉', u'休息', u'滚开']
        start_cmd = [u'出来', u'启动', u'工作']
        if self.robot_switch:
            for i in stop_cmd:
                if i == msg_data:
                    self.robot_switch = False
                    self.send_msg_by_uid(u'[Robot]' + u'机器人已关闭！', msg['to_user_id'])
        else:
            for i in start_cmd:
                if i == msg_data:
                    self.robot_switch = True
                    self.send_msg_by_uid(u'[Robot]' + u'机器人已开启！', msg['to_user_id'])

    def handle_msg_all(self, msg):
        if not self.robot_switch and msg['msg_type_id'] != 1:
            return
        if msg['msg_type_id'] == 1 and msg['content']['type'] == 0:  # reply to self
            self.auto_switch(msg)
        elif msg['msg_type_id'] == 4 and msg['content']['type'] == 0:  # text message from contact
            # print len(msg['content']['data'])
            if len(msg['content']['data']) > 10:
                if '' + msg['user']['name'] != u'\u8d85\u7ea7\u77ff\u8d44\u6e90':
                    try:
                        # TODO 提交给服务器
                        s = re.match("[\s\S]*[0-9]{11}[\s\S]*", msg['content']['data'])
                        print s, type(s)
                        if str(s) == 'None':
                            c_string = self.to_unicode('不匹配，抛弃')
                            print '********[' + c_string + ']********'
                            self.send_msg_by_uid(u'请您在要转发的消息后留下手机号', msg['user']['id'])
                        else:
                            print '--------[' + self.to_unicode('匹配') + ']--------'
                            self.post_cjkzy_msg(msg['content'], msg['user']['name'])
                            self.send_msg_by_uid(u'您的消息我已收到', msg['user']['id'])
                    except UnicodeEncodeError:
                        print '    %s[Text] (illegal text).' % msg['user']['name']
                else:
                    print '~~~~~~~~[' + self.to_unicode('自消息，已过滤') + ']~~~~~~~~'
            else:
                self.send_msg_by_uid(self.tuling_auto_reply(msg['user']['id'], msg['content']['data']), msg['user']['id'])
        elif msg['msg_type_id'] == 3 and msg['content']['type'] == 0:  # group text message
            if 'detail' in msg['content']:
                my_names = self.get_group_member_name(self.my_account['UserName'], msg['user']['id'])
                if my_names is None:
                    my_names = {}
                if 'NickName' in self.my_account and self.my_account['NickName']:
                    my_names['nickname2'] = self.my_account['NickName']
                if 'RemarkName' in self.my_account and self.my_account['RemarkName']:
                    my_names['remark_name2'] = self.my_account['RemarkName']

                is_at_me = False
                for detail in msg['content']['detail']:
                    if detail['type'] == 'at':
                        for k in my_names:
                            if my_names[k] and my_names[k] == detail['value']:
                                is_at_me = True
                                break
                if is_at_me:
                    src_name = msg['content']['user']['name']
                    reply = 'to ' + src_name + ': '
                    if msg['content']['type'] == 0:  # text message
                        reply += self.tuling_auto_reply(msg['content']['user']['id'], msg['content']['desc'])
                    else:
                        reply += u"对不起，只认字，其他杂七杂八的我都不认识，,,Ծ‸Ծ,,"
                    self.send_msg_by_uid(reply, msg['user']['id'])

    def post_cjkzy_msg(self, msg_content, user_name):
        url = 'http://www.kuaimei56.com/index.php/Views/Raw/messages'
        params = {
            "content": msg_content['data'],
            "sender": user_name,
            "wx_sender": self.my_account['NickName']
        }
        r = self.session.post(url, data=json.dumps(params))
        r.encoding = 'utf-8'
        dic = json.loads(r.text)
        print '    [Response]'
        print '    -----------------------------'
        print '    | sender: %s' % user_name
        print '    | wx_sender: %s' % self.my_account['NickName']
        print '    | result_code: %s' % dic['result_code']
        print '    | reason: %s' % dic['reason']
        print '    | error_code: %s' % dic['error_code']
        print '    | result: %s' % dic['result']
        print '    -----------------------------'


def main():
    bot = TulingWXBot()
    bot.DEBUG = True
    bot.conf['qr'] = 'png'

    bot.run()


if __name__ == '__main__':
    main()
