# !/usr/bin/env python
# coding: utf-8

# from wxbot import *
#
#
# class MyWXBot(WXBot):
#     def handle_msg_all(self, msg):
#         if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
#             self.send_msg_by_uid(u'hi', msg['user']['id'])
#             #self.send_img_msg_by_uid("img/1.png", msg['user']['id'])
#             #self.send_file_msg_by_uid("img/1.png", msg['user']['id'])
# '''
#     def schedule(self):
#         self.send_msg(u'张三', u'测试')
#         time.sleep(1)
# '''
#
#
# def main():
#     bot = MyWXBot()
#     bot.DEBUG = True
#     bot.conf['qr'] = 'png'
#     bot.run()
#
#
# if __name__ == '__main__':
#     main()


# # How can loads(r) **SOMETIMES** throws exception that 'ValueError: No JSON object could be decoded'
import json

r0 = '{"result_code":"201","reason":"\u83b7\u53d6\u6570\u636e\u6210\u529f"}'
r1 = '﻿{"result_code":"201","reason":"\u83b7\u53d6\u6570\u636e\u6210\u529f"}'

# r = "{'result_code':'201','reason':'s','result':'0','message_id':'s','error_code':'0'}"
json.loads(r0)
print "-"*20
json.loads(r1)



# aList = [123, 'xyz', 'fuck', 'abc', {"name":"a"}]
#
# a = aList.pop()
# print a["name"]
# print aList.pop()
# print aList.pop()
# print aList.pop()
# print aList.pop()
# print aList.pop()

