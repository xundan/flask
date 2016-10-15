import threading
import inspect
import ctypes


def _async_raise(tid, exctype):
    """Raises an exception in the threads with id tid"""
    if not inspect.isclass(exctype):
        raise TypeError("Only types can be raised (not instances)")
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid,
                                                     ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # "if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")


class ThreadWithExc(threading.Thread):
    """A thread class that supports raising exception in the thread from
       another thread.
    """

    def _get_my_tid(self):
        """determines this (self's) thread id

        CAREFUL : this function is executed in the context of the caller
        thread, to get the identity of the thread represented by this
        instance.
        """
        if not self.isAlive():
            raise threading.ThreadError("the thread is not active")

        # do we have it cached?
        if hasattr(self, "_thread_id"):
            return self._thread_id

        # no, look for it in the _active dict
        for tid, tobj in threading._active.items():
            if tobj is self:
                self._thread_id = tid
                return tid

        # TODO: in python 2.6, there's a simpler way to do : self.ident

        raise AssertionError("could not determine the thread's id")

    def raiseExc(self, exctype):
        """Raises the given exception type in the context of this thread.

        If the thread is busy in a system call (time.sleep(),
        socket.accept(), ...), the exception is simply ignored.

        If you are sure that your exception should terminate the thread,
        one way to ensure that it works is:

            t = ThreadWithExc( ... )
            ...
            t.raiseExc( SomeException )
            while t.isAlive():
                time.sleep( 0.1 )
                t.raiseExc( SomeException )

        If the exception is to be caught by the thread, you need a way to
        check that your thread has caught it.

        CAREFUL : this function is executed in the context of the
        caller thread, to raise an excpetion in the context of the
        thread represented by this instance.
        """
        _async_raise(self._get_my_tid(), exctype)


class DemoThread(threading.Thread):
    """use sub-class to run target function, which can be killed when parent thread is stop.
    The sub-class run only when it is joint into parent's thread.
    Problem is that when target_func is never stop, parent will never have chance to stop its son"""

    def __init__(self, wx_id, target_func, timeout=2, s_args=()):
        super(DemoThread, self).__init__()
        self.stopped = False
        self.wx_id = wx_id
        self.timeout = timeout
        self.target_func = target_func
        self.s_args = s_args
        self.sub_thread = ThreadWithExc(target=self.target_func, args=self.s_args)

    def run(self):
        self.sub_thread.setDaemon(True)
        self.sub_thread.start()

        while not self.stopped:
            print self.wx_id + "[DemoThread]: i'm not stopped"
            self.sub_thread.join(self.timeout)
            print self.wx_id + "[DemoThread]: i'm time out."

        print('Thread stopped')

    def stop(self):
        print "[DemoThread]set stopped in DemoThread"
        self.stopped = True

    def is_stopped(self):
        return self.stopped

    def get_wx_id(self):
        return self.wx_id


class WxThreadCollection(object):
    def __init__(self):
        self.threads = []

    def add(self, t):
        self.threads.append(t)
        t.setDaemon(True)
        t.start()

    def kill(self, wx_id):
        print wx_id + "[WxThreadCollection]: im in kill()"
        for td in self.threads:
            if td.get_wx_id() == wx_id:
                print "find ya!"
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
