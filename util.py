def coroutine(func):
    def start(*args, **keywords):
        cr = func(*args, **keywords)
        cr.next()
        return cr
    return start
