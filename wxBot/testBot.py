#!/usr/bin/env python
# coding: utf-8

from wxbot import *


class MyWXBot(WXBot):
    def show_png(self):
        if self.env == 'ecs':
            pass

    def handle_msg_all(self, msg):
        if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
            # self.send_img_msg_by_uid("img/1.png", msg['user']['id'])
            # self.send_file_msg_by_uid("img/1.png", msg['user']['id'])
            # try:
            #     file_object = open('thefile.txt', 'w')
            #     print "*****************************lol****************************"
            #     # file_object.write(self.to_unicode("超级矿资源工作群"))
            #     # file_object.write('\n')
            #     print self.to_unicode("超级矿资源工作群")
            #     file_object.write(str(self.group_members))
            #     print "*************************writing****************************"
            #     file_object.close()
            #     file_object = open('all.txt', 'w')
            #     print "*****************************lol****************************"
            #     file_object.write(str(self.member_list))
            #     print "*************************writing****************************"
            #     file_object.close()
            #     file_object = open('group.txt', 'w')
            #     print "*****************************lol****************************"
            #     file_object.write(str(self.group_list))
            #     print "*************************writing****************************"
            #     file_object.close()
            # except Exception:
            #     print 'something happened'
            #     pass
            if '' + msg['user']['name'] != u'\u8d85\u7ea7\u77ff\u8d44\u6e90':
                try:
                    # TODO 提交给服务器
                    s = re.match("[\s\S]*[0-9]{11}[\s\S]*", msg['content']['data'])
                    print s, type(s)
                    if str(s) == 'None':
                        c_string = self.to_unicode('不匹配，转人工')
                        self.post_chat_record(msg['content'], msg['user']['name'], 0)
                        print '********[' + c_string + ']********'
                        # self.send_msg_by_uid(u'请您留下手机号', msg['user']['id'])
                    else:
                        print '--------[' + self.to_unicode('匹配') + ']--------'
                        self.post_cjkzy_msg(msg['content'], msg['user']['name'])
                        self.send_msg_by_uid(u'您的消息我已收到', msg['user']['id'])
                except UnicodeEncodeError:
                    print '    %s[Text] (illegal text).' % msg['user']['name']
            else:
                print '~~~~~~~~[' + self.to_unicode('自消息，已过滤') + ']~~~~~~~~'
        if msg['msg_type_id'] == 3 and msg['content']['type'] == 0:
            print '    (group-message): %s' % msg['content']['data']

    def schedule(self):
        # here to append manual_list
        msg2send = self.fetch_msg_to_send()
        if msg2send is not None:
            self.manual_list.append(msg2send)
        time.sleep(5)

        if len(self.manual_list) > 0:
            message = self.manual_list.pop()
            self.send_msg(message["name"], message["word"])
            self.update_chat_msg_sent(message["id"])
        else:
            print self.wx_id + " Nothing to send now."

    def fetch_msg_to_send(self):
        url = 'http://www.kuaimei56.com/index.php/Views/ChatRecord/unsent_record'
        params = {
            "self_wx": self.wx_id
        }
        r = self.session.post(url, data=json.dumps(params))
        print "r.encoding", r.encoding
        # r.encoding = 'ISO-8859-1'
        dic = json.loads(r.text)

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
        print u"[Error] [fetch_msg_to_send] 数据库错误:" + dic['result_code']
        return None

    def update_chat_msg_sent(self, record_id):
        url = 'http://www.kuaimei56.com/index.php/Views/ChatRecord/status'
        params = {
            "id": record_id,
            "status": 1
        }
        r = self.session.post(url, data=json.dumps(params))
        r.encoding = 'utf-8'
        dic = json.loads(r.text)
        print '    [Response]'
        print '    -----------------------------'
        print '    | result_code: %s' % dic['result_code']
        print '    | reason: %s' % dic['reason']
        print '    | error_code: %s' % dic['error_code']
        print '    | result: %s' % dic['result']
        print '    -----------------------------'

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

    def post_chat_record(self, msg_content, user_name, isme=0):
        url = 'http://www.kuaimei56.com/index.php/Views/ChatRecord/record'
        params = {
            "self_wx": self.wx_id,
            "client_name": user_name,
            "content": msg_content['data'],
            "isme": isme,
            "type": "plain",
            "remark": "0"
        }
        r = self.session.post(url, data=json.dumps(params))
        r.encoding = 'utf-8'
        dic = json.loads(r.text)
        print '    [Response]'
        print '    -----------------------------'
        print '    | client_name: %s' % user_name
        print '    | self_wx: %s' % self.wx_id
        print '    | result_code: %s' % dic['result_code']
        print '    | reason: %s' % dic['reason']
        print '    | error_code: %s' % dic['error_code']
        print '    | result: %s' % dic['result']
        print '    -----------------------------'


def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.run()


if __name__ == '__main__':
    main()
