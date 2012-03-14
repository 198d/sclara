import unittest
from greenlet import greenlet

from sclara import default_app
from .test import test, description


class GreenSuite(unittest.TestSuite):
    def __iter__(self):
        while True:
            case = greenlet.getcurrent().parent.switch()
            if case:
                yield case
            else:
                raise StopIteration


class green_test(test):
    def __exit__(self, *args):
        default_app.runner.glet.switch(default_app.cases.pop())
        return super(green_test, self).__exit__(*args)


class runner(object):
    def __init__(self):
        self.test = test
        self.description = description

    def __enter__(self):
        default_app.runners.append(self)
        return self

    def __exit__(self, *args):
        default_app.runners.pop()


class delayed_runner(runner):
    def __exit__(self, *args):
        super(delayed_runner, self).__exit__(*args)
        suite = unittest.TestSuite(default_app.cases)
        unittest.TextTestRunner().run(suite)


class greenlet_runner(runner):
    def __init__(self):
        super(greenlet_runner, self).__init__()
        self.test = green_test
        self.glet = greenlet(self.run)
        self.glet.switch()

    def __exit__(self, *args):
        super(greenlet_runner, self).__exit__(*args)
        self.glet.switch()

    def run(self):
        suite = GreenSuite()
        unittest.TextTestRunner().run(suite)
