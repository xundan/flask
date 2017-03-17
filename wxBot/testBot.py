#!/usr/bin/env python
# coding: utf-8
import apiUtils
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
                    p = re.compile(r'[\s\S]*([0-9]{11})[\s\S]*')
                    finds = p.findall(msg['content']['data'])
                    if len(finds) == 0:
                        c_string = self.to_unicode('不匹配，转人工')
                        apiUtils.post_chat_record(self.wx_id, msg['content'], msg['user']['name'], 0, "plain")
                        print '********[' + c_string + ']********'
                        # self.send_msg_by_uid(u'请您留下手机号', msg['user']['id'])
                    else:
                        print '--------[' + self.to_unicode('匹配') + ']--------'
                        apiUtils.post_cjkzy_msg(self.wx_id, msg['content'], msg['user']['name'], finds[0])
                        apiUtils.post_chat_record(self.wx_id, msg['content'], msg['user']['name'], 0, "msg")
                        time.sleep(2)
                        self.send_msg_by_uid(u'您的消息我已收到', msg['user']['id'])
                except UnicodeEncodeError:
                    print '    %s[Text] (illegal text).' % msg['user']['name']
            else:
                print '~~~~~~~~[' + self.to_unicode('自消息，已过滤') + ']~~~~~~~~'
        # if msg['msg_type_id'] == 3 and msg['content']['type'] == 0:
        #     print '    (group-message): %s' % msg['content']['data']

        # 群消息
        # if msg['msg_type_id'] == 3 and msg['content']['type'] == 0:
        #     try:
        #         p = re.compile(r'[\s\S]*([0-9]{11})[\s\S]*')
        #         finds = p.findall(msg['content']['data'])
        #         if len(finds) == 0:
        #             print '--------[' + self.to_unicode('匹配') + ']--------'
        #             apiUtils.post_cjkzy_msg(self.wx_id, msg['content'], '[q]'+msg['user']['name'], finds[0])
        #             # apiUtils.post_chat_record(self.wx_id, msg['content'], msg['user']['name'], 0, "msg")
        #             # self.send_msg_by_uid(u'您的消息我已收到', msg['user']['id'])
        #     except UnicodeEncodeError:
        #         print '    %s[Text] (illegal text).' % msg['user']['name']

    def schedule(self):
        pass
        # # here to append manual_list
        # msg2send = apiUtils.fetch_msg_to_send(self.wx_id)
        # if msg2send is not None:
        #     self.manual_list.append(msg2send)
        # # time.sleep(2)
        #
        # if len(self.manual_list) > 0:
        #     message = self.manual_list.pop()
        #     self.send_msg(message["name"], message["word"])
        #     apiUtils.update_chat_msg_sent(message["id"])
        # # else:
        # #     print self.wx_id + " Nothing to send now."


def main():
    bot = MyWXBot()
    bot.DEBUG = True
    bot.run()
    # r1 = '﻿{"result_code":"201","reason":"\u83b7\u53d6\u6570\u636e\u6210\u529f"}'
    # text = bot.delete_bom(r1)
    # json.loads(text)
    # r0 = '{"result_code":"201","reason":"\u83b7\u53d6\u6570\u636e\u6210\u529f"}'
    # text = bot.delete_bom(r0)
    # json.loads(text)

if __name__ == '__main__':
    main()
