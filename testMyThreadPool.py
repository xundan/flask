# Test
from myThreadPool import ThreadPool, WorkRequest, NoResultsPending

if __name__=='__main__':
    import random
    import time
    import datetime

    def do_work(data):
        time.sleep(random.randint(1,3))
        res = str(datetime.datetime.now())+""+str(data)
        return res

    def print_result(request, result):
        print "***Result from request %s : %r" % (request.request_id, result)

    main = ThreadPool(3)
    for i in range(40):
        req = WorkRequest(do_work, args=[i], kwds={}, callback=print_result)
        main.put_request(req)
        print "+++Work request #%s added." % req.request_id

    print '-'*20, main.worker_size(), '-'*20

    counter = 0
    while True:
        try:
            time.sleep(0.5)
            main.poll()
            if (counter == 5):
                print "Add 3 more working threads."
                main.create_workers(3)
                print '-' * 20, main.worker_size(), '-' * 20
            if (counter == 10):
                print "Dismiss 2 working threads."
                main.dismiss_workers(2)
                print '-' * 20, main.worker_size(), '-' * 20
            counter += 1
        except NoResultsPending:
            print "No Pending RESULTS"
            break

    main.stop()
    print "Stop"

