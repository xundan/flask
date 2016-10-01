# -*-encoding:utf-8-*-
'''
Advanced Thread Pool
'''

import sys
import threading
import Queue
import traceback


# 定义一些异常，用于自定义异常处理


class NoResultsPending(Exception):
    """All work requests have been processed"""
    pass


class NoWorkersAvailable(Exception):
    """No working threads available to process remaining requests"""
    pass


def _handle_thread_exception(request, exc_info):
    """Handle exceptions defaultly, only by printing them out."""
    traceback.print_exception(*exc_info)


# classes


class WorkerThread(threading.Thread):
    """Thread, get work from request_queue,
    return results when work done and put results in result_queue"""

    def __init__(self, request_queue, result_queue, poll_timeout=5, **kwds):
        threading.Thread.__init__(self, **kwds)
        '''Set as guard-thread'''
        self.setDaemon(True)
        self._request_queue = request_queue
        self._result_queue = result_queue
        self._poll_timeout = poll_timeout
        '''A flag that whether this thread should be dismissed, default as false'''
        self._dismissed = threading.Event()
        self.start()

    def run(self):
        """Every thread do the work as much as possible, that's why use loop.
        If thread is available, and there is work not-done in request_queue, loop will keep running."""
        while True:
            if self._dismissed.is_set():
                break
            try:
                '''Queue.Queue use thread sync strategy, and timeout can be set.
                Thread will block, until request_queue has some works, unless time is out'''
                request = self._request_queue.get(True, self._poll_timeout)
            except Queue.Empty:
                continue
            else:
                '''Recheck the dismissed here, for the possibility that thread may be dismissed
                before the time is out.'''
                if self._dismissed.is_set():
                    self._request_queue.put(request)
                    break
                try:
                    '''Run the callable, put requests and results into request_queue as tuple.'''
                    result = request.callable(*request.args, **request.kwds)
                    print "L69 self.getName(): " + self.getName()
                    self._result_queue.put((request, result))
                except:
                    '''Handle the exception.'''
                    request.exception = True
                    self._result_queue.put((request, sys.exc_info()))

    def dismiss(self):
        """Set a flag as completing current work, then quit."""
        self._dismissed.set()


class WorkRequest:
    """
    @:param callable_: customizable, run the work.
    @:param args: param list
    @:param kwds: dict list
    @:param request_id: id
    @:param callback: customizable, function for elements in result_queue
    @:param exc_callback: customizable, handle exceptions
    """

    def __init__(self, callable_, args=None, kwds=None, request_id=None,
                 callback=None, exc_callback=_handle_thread_exception):
        if request_id == None:
            self.request_id = id(self)
        else:
            try:
                self.request_id = hash(request_id)
            except TypeError:
                raise TypeError("request_id must be hashable.")
        self.exception = False
        self.callback = callback
        self.exc_callback = exc_callback
        self.callable = callable_
        self.args = args or []
        self.kwds = kwds or {}

    def __str__(self):
        return "WorkRequest id=%s args=%r kwargs=%r exception=%s" % \
               (self.request_id, self.args, self.kwds, self.exception)


class ThreadPool:
    """
    :param num_workers: number of initial threads
    :param q_size, resq_size: size of request_queue and result_queue
    :param poll_timeout: set timeout of WorkerThread, as same as timeout of waiting request_queue
    """

    def __init__(self, num_workers, q_size=0, resq_size=0, poll_timeout=5):
        self._request_queue = Queue.Queue(q_size)
        self._result_queue = Queue.Queue(resq_size)
        self.workers = []
        self.dismissed_workers = []
        self.work_requests = {}
        self.create_workers(num_workers, poll_timeout)

    def create_workers(self, num_workers, poll_timeout=5):
        """create workers with number of num_workers and timeout with poll_timeout"""
        for i in range(num_workers):
            self.workers.append(WorkerThread(self._request_queue, self._result_queue, poll_timeout=poll_timeout))

    def dismiss_workers(self, num_workers, do_join=False):
        """stop workers with size of num_workers, add them to dismiss_list"""
        dismiss_list = []
        for i in range(min(num_workers, len(self.workers))):
            worker = self.workers.pop()
            worker.dismiss()
            dismiss_list.append(worker)
        if do_join:
            for worker in dismiss_list:
                worker.join()
        else:
            self.dismissed_workers.extend(dismiss_list)

    def join_all_dismissed_workers(self):
        """join all stopped thread"""
        for worker in self.dismissed_workers:
            worker.join()
        self.dismissed_workers = []

    def put_request(self, request, block=True, timeout=None):
        assert isinstance(request, WorkRequest)
        assert not getattr(request, 'exception', None)
        '''If queue is full of its size, which is q_size,
        it will be blocked, until it has some room or time is out.'''
        self._request_queue.put(request, block, timeout)
        self.work_requests[request.request_id] = request

    def poll(self, block=False):
        while True:
            if not self.work_requests:
                raise NoResultsPending
            elif block and not self.workers:
                raise NoWorkersAvailable
            try:
                '''get result_queue's value only when it has value,
                otherwise there always be blocked.'''
                request, result = self._result_queue.get(block=block)
                if request.exception and request.exc_callback:
                    request.exc_callback(request, result)
                if request.callback and not (request.exception and request.exc_callback):
                    request.callback(request, result)
                del self.work_requests[request.request_id]
            except Queue.Empty:
                break

    def wait(self):
        while True:
            try:
                self.poll(True)
            except NoResultsPending:
                break

    def worker_size(self):
        return len(self.workers)

    def stop(self):
        """join all thread, make sure all thread are done."""
        self.dismiss_workers(self.worker_size(),True)
        self.join_all_dismissed_workers()
