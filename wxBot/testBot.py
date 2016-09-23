#!/usr/bin/env python
# coding: utf-8

from wxbot import *


class MyWXBot(WXBot):
    def show_png(self):
        if self.env == 'ecs':
            pass

    def handle_msg_all(self, msg):
        if msg['msg_type_id'] == 4 and msg['content']['type'] == 0 and msg['content']['data'] == '1':
            # self.send_img_msg_by_uid("img/1.png", msg['user']['id'])
            # self.send_file_msg_by_uid("img/1.png", msg['user']['id'])
            try:
                file_object = open('thefile.txt', 'w')
                print "*****************************lol****************************"
                # file_object.write(self.to_unicode("超级矿资源工作群"))
                # file_object.write('\n')
                print self.to_unicode("超级矿资源工作群")
                file_object.write(str(self.group_members))
                print "*************************writing****************************"
                file_object.close()
                file_object = open('all.txt', 'w')
                print "*****************************lol****************************"
                file_object.write(str(self.member_list))
                print "*************************writing****************************"
                file_object.close()
                file_object = open('group.txt', 'w')
                print "*****************************lol****************************"
                file_object.write(str(self.group_list))
                print "*************************writing****************************"
                file_object.close()
            except Exception:
                print 'something happened'
                pass
            if '' + msg['user']['name'] != u'\u8d85\u7ea7\u77ff\u8d44\u6e90':
                try:
                    # TODO 提交给服务器
                    s = re.match("[\s\S]*[0-9]{11}[\s\S]*", msg['content']['data'])
                    print s, type(s)
                    if str(s) == 'None':
                        c_string = self.to_unicode('不匹配，抛弃')
                        print '********[' + c_string + ']********'
                        self.send_msg_by_uid(u'请您留下手机号', msg['user']['id'])
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

    # def schedule(self):
    #     self.send_msg(u'荀辰龙', u'schedule')
    #     time.sleep(1)

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
    bot = MyWXBot()
    bot.DEBUG = True
    bot.run()


if __name__ == '__main__':
    main()
