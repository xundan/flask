import threading
from wxBot.testBot import MyWXBot


class DemoThread(threading.Thread):
    """use sub-class as demon thread, can be close."""

    def __init__(self, wx_id, timeout=2):
        super(DemoThread, self).__init__()
        self.stopped = False
        self.wx_id = wx_id
        self.timeout = timeout
        self.bot = None
        self.sub_thread = threading.Thread(target=self.login_wx, args=())

    def run(self):
        self.sub_thread.setDaemon(True)
        self.sub_thread.start()

        while not self.stopped:
            self.sub_thread.join(self.timeout)

        print "thread stopped"

    def login_wx(self):
        print "now start wxbot by flask with: " + self.wx_id
        self.bot = MyWXBot(self.wx_id)
        self.bot.DEBUG = True
        self.bot.run()

    def stop(self):
        # print "im here! stopped is true."
        self.stopped = True
        if self.bot is not None:
            self.bot.set_running(False)

    def is_stopped(self):
        return self.stopped

    def get_wx_id(self):
        return self.wx_id


class WxThreadCollection(object):
    def __init__(self):
        self.threads = []

    def add(self, t):
        self.threads.append(t)
        # t.setDaemon(True)
        t.start()

    def kill(self, wx_id):
        print wx_id + " [WxThreadCollection]: im in kill()"
        for td in self.threads:
            if td.get_wx_id() == wx_id:
                print "find ya!"
                td.stop()
                # td.join()
                self.threads.remove(td)
                break


# thread2 = DemoThread(wx_id="test002")
# thread2.start()
# time.sleep(35)
# thread2.stop()
# while True:
#     print "live"
#     time.sleep(0.5)

