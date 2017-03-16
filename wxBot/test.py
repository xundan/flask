# !/usr/bin/env python
# coding: utf-8

from wxbot import *
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


# How can loads(r) **SOMETIMES** throws exception that 'ValueError: No JSON object could be decoded'
import json

# r0 = '{"result_code":"201","reason":"\u83b7\u53d6\u6570\u636e\u6210\u529f"}'
# r1 = '﻿{"result_code":"201","reason":"\u83b7\u53d6\u6570\u636e\u6210\u529f"}'
# json.loads(r0)
# print "-"*20
# json.loads(r1)
from wxBot.testBot import MyWXBot

# aList = [123, 'xyz', 'fuck', 'abc', {"name":"a"}]
# bList={}
# bList['a']=aList
# bList['b']="a"

#
# a = aList.pop()
# print a["name"]
# print aList.pop()
# print aList.pop()
# print aList.pop()
# print aList.pop()
# print aList.pop()

# a = json.dumps(aList)
# print a
# a = json.dumps(bList)
# print a
# a = MyWXBot.delete_bom(a)
# b = json.loads(a)


# s = re.match("[\s\S]*[0-9]{11}[\s\S]*", u"a【】12341234123 aba")
# print s, type(s)
# if s is not None:
#     print s.group()

p = re.compile(r'[\s\S]*([0-9]{11})[\s\S]*')
arr = p.findall(u"a【】12341234123 aba")
print len(arr)
arr2 = p.findall(u"a【】1234134123 aba")
print len(arr2)

print str('str')