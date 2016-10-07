import threading


class DemoThread(threading.Thread):
    """use sub-class to run target function, which can be killed when parent thread is stop"""
    def __init__(self, target_func, timeout=1.0, s_args=()):
        super(DemoThread, self).__init__()
        self.stopped = False
        self.timeout = timeout
        self.target_func = target_func
        self.s_args = s_args

    def run(self):
        sub_thread = threading.Thread(target=self.target_func, args=self.s_args)
        sub_thread.setDaemon(True)
        sub_thread.start()

        while not self.stopped:
            sub_thread.join(self.timeout)

        print('Thread stopped')

    def stop(self):
        self.stopped = True

    def is_stopped(self):
        return self.stopped

    def get_name(self):
        return self.name


class WxThreadCollection(object):
    def __init__(self):
        self.threads = []

    def add(self, t):
        self.threads.append(t)
        t.setDaemon(True)
        t.start()

    def kill(self, name):
        for td in self.threads:
            if td.get_name() == name:
                td.stop()
                self.threads.remove(td)
                break


# def foo(name="default"):
#     # inp = raw_input("Thread : ")
#     # print('Thread input %s' % inp)
#     time.sleep(2)
#     print name+str(200 * 300)
#
#
# threads = []
# thread = DemoThread(target_func=foo, s_args=('wx001',))
# threads.append(thread)
#
# for t1 in threads:
#     t1.setDaemon(True)
#     t1.start()
#
# print('Main thread Waiting')
# time.sleep(3)
#
# print "now still in Main"
