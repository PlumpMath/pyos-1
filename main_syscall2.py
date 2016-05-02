from pyos import *

def foo():
    mytid = yield GetTid()
    while True:
        print "I'm foo", mytid
        yield


def main():
    child = yield NewTask(foo())
    for i in xrange(5):
        yield

    isKilled = yield KillTask(child)
    print "Task %d is %s" % (child,  "killed" if isKilled else "still alive")
    print "main done"

sched = Scheduler()
sched.new(main())
sched.mainloop()

# output:

# I'm foo 2
# I'm foo 2
# I'm foo 2
# I'm foo 2
# I'm foo 2
# Task 2 terminated
# main done
# Task 1 terminated
