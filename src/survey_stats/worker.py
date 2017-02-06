import rq

# rq worker
with rq.Connection():
    qs = list(map(['high', 'normal', 'low']))
    w = rq.Worker(qs)
    w.work()


