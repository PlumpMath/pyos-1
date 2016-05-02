from Queue import Queue

class Task(object):
    """A task is a wrapper around a coroutine"""
    taskid = 0
    def __init__(self, target):
        Task.taskid += 1
        self.tid = Task.taskid
        self.target = target
        self.sendval = None

    # Run a task until it hits the next yield statement
    def run(self):
        # print "Task %d is send {%s} ....." % (self.tid, self.sendval)
        return self.target.send(self.sendval)


class Scheduler(object):

    def __init__(self):
        self.ready = Queue()
        self.taskmap = {}
        self.exit_waiting = {}

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
        for task in self.exit_waiting.pop(task.tid, []):
            self.schedule(task)


    def waitforexit(self, task, waittid):
        if waittid in self.taskmap:
            self.exit_waiting.setdefault(waittid, []).append(task)
            return True
        else:
            return False

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

class NewTask(SystemCall):

    def __init__(self, target):
        self.target = target

    def handler(self):
        tid = self.sched.new(self.target)
        self.task.sendval = tid
        self.sched.schedule(self.task)

class KillTask(SystemCall):

    def __init__(self, tid):
        self.tid = tid

    def handler(self):
        task = self.sched.taskmap.get(self.tid, None)
        if task:
            task.target.close()
            self.task.sendval = True
        else:
            self.task.sendval = False

        self.sched.schedule(self.task)

class WaitTask(SystemCall):
    def __init__(self, tid):
        self.tid = tid

    def handler(self):
        result = self.sched.waitforexit(self.task, self.tid)
        self.task.sendval = result
        # If waiting for a non-existent task,
        # return immediately without waiting
        if not result:
            self.sched.schedule(task)
