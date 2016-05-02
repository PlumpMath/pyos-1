from pyos import *

def foo():
    for i in xrange(5):
        print "I'm foo"
        yield

def main():
    child = yield NewTask(foo())
    print "Waiting for child"
    yield WaitTask(child)
    print "Child done"

sched = Scheduler()
sched.new(main())
sched.mainloop()

# output:

# I'm foo
# Waiting for child
# I'm foo
# I'm foo
# I'm foo
# I'm foo
# Task 2 terminated
# Child done
# Task 1 terminated
