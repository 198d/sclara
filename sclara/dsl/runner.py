import unittest
from greenlet import greenlet

from .test import test
from sclara import default_app


class GreenSuite(unittest.TestSuite):
    def __iter__(self):
        while True:
            case = greenlet.getcurrent().parent.switch()
            if case:
                yield case
            else:
                raise StopIteration


class simple_runner(object):
    def __enter__(self):
        return default_app.description, default_app.test

    def __exit__(self, *args):
        suite = unittest.TestSuite(default_app.cases)
        unittest.TextTestRunner().run(suite)


class greenlet_runner(object):
    def __enter__(self):
        default_app.test = green_test
        green_test.glet = greenlet(self.runner)
        green_test.glet.switch()
        return default_app.description, default_app.test

    def __exit__(self, *args):
        green_test.glet.switch()

    def runner(self):
        suite = GreenSuite()
        unittest.TextTestRunner().run(suite)


class green_test(test):
    glet = None

    def __exit__(self, *args):
        super(green_test, self).__exit__(*args)
        self.glet.switch(default_app.cases.pop())
        return True
