import time


class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, *args):
        self.end = time.time()
        self.secs = self.end - self.start
        self.msecs = self.secs * 1000  # millisecs
        if self.verbose:
            print('elapsed time: {:>10.0f} ms'.format(self.msecs))


class Measure(object):
    def __init__(self):
        self.times = []

    def append(self, t):
        self.times.append(t)

    def __repr__(self):
        return 'min{:>7.0f} ||   max{:>7.0f} ||   avg{:>7.0f}'.format( min(self.times), max(self.times), sum(self.times) / len(self.times))
