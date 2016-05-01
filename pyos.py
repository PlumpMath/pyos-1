from Queue import Queue

class Task(object):
    """A task is a wrapper around a coroutine"""
    taskid = 0
    def __init__(self, target):
        Task.taskid += 1
        self.tid = Task.taskid
        self.target = target   # target coroutine
        self.sendval = None


    def run(self):
        return self.target.send(self.sendval)


class Scheduler(object):

    def __init__(self):
        self.ready = Queue()
        self.taskmap = {}

    def new(self, target):
        newtask = Task(target)
        self.taskmap[newtask.taskid] = newtask
        self.schedule(newtask)
        return newtask.taskid

    def schedule(self, task):
        self.ready.put(task)

    def exit(self, task):
        print "Task %d terminated" % task.tid
        del self.taskmap[task.tid]

    def mainloop(self):
        while self.taskmap:
            task = self.ready.get()
            try:
                result = task.run()
                if isinstance(result, SystemCall):
                    result.task = task
                    result.sched = self
                    result.handler()
                    continue
            except StopIteration:
                self.exit(task)
                continue

            self.schedule(task)


class SystemCall(object):
    def handler(self):
        pass


class GetTid(SystemCall):
    def handler(self):
        self.task.sendval = self.task.tid
        self.sched.schedule(self.task)
