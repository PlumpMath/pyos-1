from pyos import *


def foo():
    while True:
        print "I'm foo"
        yield

def bar():
    while True:
        print "I'm bar"
        yield

def foo():
    for i in xrange(10):
        print "I'm foo"
        yield
def bar():
    for i in xrange(5):
        print "I'm bar"
        yield


def foo():
    mytid = yield GetTid()
    for i in xrange(5):
        print "I'm foo", mytid
        yield

def bar():
    mytid = yield GetTid()
    for i in xrange(10):
        print "I'm bar", mytid
        yield

sched = Scheduler()
sched.new(foo())
sched.new(bar())
sched.mainloop()
