from pyos import Scheduler
from echo_server import server


def alive():
    while True:
        print "I'm alive!"
        yield


sched = Scheduler()
#sched.new(alive())
sched.new(server(45000))
sched.mainloop()
