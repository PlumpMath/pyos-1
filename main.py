from pyos import *

"""
Basic schedule
"""

def foo():
    for i in xrange(10):
        print "I'm foo"
        yield

        
def bar():
    for i in xrange(5):
        print "I'm bar"
        yield

sched = Scheduler()
sched.new(foo())
sched.new(bar())
sched.mainloop()

# output:

# I'm foo
# I'm bar
# I'm foo
# I'm bar
# I'm foo
# I'm bar
# I'm foo
# I'm bar
# I'm foo
# I'm bar
# I'm foo
# Task 2 terminated
# I'm foo
# I'm foo
# I'm foo
# I'm foo
# Task 1 terminated
