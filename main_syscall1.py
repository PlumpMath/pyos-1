from pyos import *

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

# output:

# I'm foo 1
# I'm bar 2
# I'm foo 1
# I'm bar 2
# I'm foo 1
# I'm bar 2
# I'm foo 1
# I'm bar 2
# I'm foo 1
# I'm bar 2
# Task 1 terminated
# I'm bar 2
# I'm bar 2
# I'm bar 2
# I'm bar 2
# I'm bar 2
# Task 2 terminated
