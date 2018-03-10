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
            #     for i in self.group_list:
            #         print str(i)
            #     print "*************************writing****************************"
            #     file_object.close()
            # except Exception:
            #     print 'something happened'
            #     pass
            try:
                p = re.compile(r'[\s\S]*([0-9]{11})[\s\S]*')
                finds = p.findall(msg['content']['data'])
                if len(finds) == 0:
                    c_string = self.to_unicode('不匹配，转人工')
                    # apiUtils.post_chat_record(self.wx_id, msg['content'], msg['user']['name'], 0, "plain")
                    print '********[' + c_string + ']********'
                    # self.send_msg_by_uid(u'请您留下手机号', msg['user']['id'])
                else:
                    print '--------[' + self.to_unicode('匹配') + ']--------'
                    # apiUtils.post_cjkzy_msg(self.wx_id, msg['content'], msg['user']['name'], finds[0])
                    # apiUtils.post_chat_record(self.wx_id, msg['content'], msg['user']['name'], 0, "msg")
                    # time.sleep(2)
                    # if self.wx_id=="cjkzy001" or self.wx_id=="cjkzy003" or self.wx_id=="cjkzy005" or self.wx_id=="cjkzy007" or self.wx_id=="cjkzywl":
                    #     self.send_msg_by_uid(u'您的消息我已收到', msg['user']['id'])
                    # else:
                    #     self.send_msg_by_uid(u'您好，您的消息已收到。请扫描下方二维码关注超级矿资源公众号，您可以发布、查看煤炭供求、找车信息，您还可以把我们的公众号推荐给您身边做煤炭的朋友，我们可以把您的信息做置顶发布。', msg['user']['id'])
                    #     time.sleep(1)
                    #     self.send_img_msg_by_uid(os.path.join(self.temp_pwd, 'cjkzy_mp.jpg'), msg['user']['id'])
                    # self.send_msg_by_uid(u'您的消息我已收到', msg['user']['id'])
            except UnicodeEncodeError:
                print '    %s[Text] (illegal text).' % msg['user']['name']
            # 是否符合查询语句
            # try:
            #     # p = re.compile(r'$[012345求车购供应查询]')
            #     # finds = p.findall(msg['content']['data'])
            #     if len(msg['content']['data']) > 30:
            #         pass
            #     else:
            #         print '--------[' + self.to_unicode('query匹配') + ']--------'
            #         print msg['content']['data']
            #         result = apiUtils.fetch_query_text(msg['content']['data'], msg['user']['id'], self.wx_id)
            #         if result:
            #             self.send_msg_by_uid(self.to_unicode(result), msg['user']['id'])
            # except UnicodeEncodeError:
            #     print '    %s[Text] (illegal text 2).' % msg['user']['name']
        # 群消息
        if msg['msg_type_id'] == 3 and msg['content']['type'] == 0:
            try:
                p = re.compile(r'[\s\S]*([0-9]{11})[\s\S]*')
                finds = p.findall(msg['content']['data'])
                if len(finds) == 0:
                    pass
                else:
                    if u'A 矿【转发信息】群'!=msg['user']['name']: # 排除自己的转发群
                        for i in self.group_list:
                            print str(i)
                        print '--------[' + self.to_unicode('群匹配') + ']--------'
                        # apiUtils.post_cjkzy_msg(self.wx_id, msg['content'], '[q]'+msg['user']['name'], finds[0])
                        print 'Now user_name is: '+msg['user']['name']
                        print '***'
                        print msg['user']
                        print '***'
                        print msg
                        if u'测试群回复' == msg['user']['name']:
                            print u'在测试群里了。'
                            # self.send_msg_by_uid(u'您的消息已收到，超级矿资源平台会尽快帮您转发消息。', msg['user']['id'])
                        else:
                            pass
                    else:
                        print u'自己群消息'
            except UnicodeEncodeError:
                print '    %s[Text] (illegal text).' % msg['user']['name']

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
