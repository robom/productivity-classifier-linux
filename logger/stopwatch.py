from logger.dependencies import *


class Stopwatch:
    # def __init__(self, func=time.perf_counter):
    def __init__(self, func=timeit.default_timer):
        self.elapsed = 0.0
        self._func = func
        self._start = None
        self._last_active = None

    def start(self):
        self.remove_afk()
        if self._start is None:
            self._start = self._func()
        self._last_active = self._func()

    def stop(self):
        if self._start is not None:
            self.remove_afk()
            end = self._func()
            self.elapsed += end - self._start
            self._start = None
            self._last_active = None

    def ping(self):
        self.remove_afk()
        self.start()

    def remove_afk(self):
        if (self._last_active is not None and self._func() - self._last_active) > 120:
            self.elapsed += self._last_active - self._start + 120
            self._start = self._func()
            self._last_active = self._func()

    def reset(self):
        self.elapsed = 0.0

    @property
    def running(self):
        return self._start is not None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()
