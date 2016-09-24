import threading


class WorkerTask(object):
    """A task to be performed by the ThreadPool."""

    def __init__(self, name, function, args=(), kwargs={}):
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.name = name

    def __call__(self):
        self.function(*self.args, **self.kwargs)

    def get_name(self):
        return self.name


class WorkerThread(threading.Thread):
    """A thread managed by a thread pool."""

    def __init__(self, pool, name):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.pool = pool
        self.busy = False
        self._started = False
        self._event = None
        self.name = name

    def get_name(self):
        return self.name

    def work(self):
        if self._started is True:
            if self._event is not None and not self._event.isSet():
                self._event.set()
        else:
            self._started = True
            self.start()

    def run(self):
        while True:
            self.busy = True
            while len(self.pool._tasks) > 0:
                try:
                    task = self.pool._tasks.pop()
                    task()
                except IndexError:
                    # Just in case another thread grabbed the task 1st.
                    pass

                    # Sleep until needed again
            self.busy = False
            if self._event is None:
                self._event = threading.Event()
            else:
                self._event.clear()
            self._event.wait()


class ThreadPool(object):
    """Executes queued tasks in the background."""

    def __init__(self, max_pool_size=20):
        self.max_pool_size = max_pool_size
        self._threads = []
        self._tasks = []

    def _addTask(self, task):
        self._tasks.append(task)

        name = task.get_name()
        worker_thread = None
        for thread in self._threads:
            if thread.busy is False:
                worker_thread = thread
                break

        if worker_thread is None and len(self._threads) <= self.max_pool_size:
            worker_thread = WorkerThread(self, name)
            self._threads.append(worker_thread)

        if worker_thread is not None:
            worker_thread.work()

    def addTask(self, name, function, args=(), kwargs={}):
        self._addTask(WorkerTask(name, function, args, kwargs))

    def killTask(self, name):
        for thread in self._threads:
            if thread.get_name() == name:
                self._threads.remove(thread)
                thread.join()
                # thread.join()
                # thread = None



class GlobalThreadPool(object):
    """ThreadPool Singleton class."""

    _instance = None

    def __init__(self):
        """Create singleton instance """

        if GlobalThreadPool._instance is None:
            # Create and remember instance
            GlobalThreadPool._instance = ThreadPool()

    def __getattr__(self, attr):
        """ Delegate get access to implementation """
        return getattr(self._instance, attr)

    def __setattr__(self, attr, val):
        """ Delegate set access to implementation """
        return setattr(self._instance, attr, val)
