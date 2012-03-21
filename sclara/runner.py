import unittest
from greenlet import greenlet

from sclara.session import session


class GreenSuite(unittest.TestSuite):
    def __iter__(self):
        while True:
            case = greenlet.getcurrent().parent.switch()
            if case:
                yield case
            else:
                raise StopIteration


class test_runner(object):
    def __init__(self, desc=''):
        self.desc = desc
        self.cases = []

    def __enter__(self):
        session.push(self, 'runner')
        return self

    def __exit__(self, *args):
        session.pop()

    def handle_result(self, exc_info):
        type_, value, traceback = exc_info

        if type_:
            def test_method(self):
                raise type_, value, traceback
        else:
            def test_method(self):
                pass
        test_method.__name__ = session.description
        test_method.__doc__ = session.description

        test_case_class = type("TestCase", (unittest.TestCase,),
            {test_method.__name__: test_method})
        test_case = test_case_class(test_method.__name__)

        self.cases.append(test_case)


class delayed_runner(test_runner):
    def __exit__(self, *args):
        super(delayed_runner, self).__exit__(*args)
        suite = unittest.TestSuite(self.cases)
        unittest.TextTestRunner().run(suite)


class greenlet_runner(test_runner):
    def __init__(self, desc=''):
        super(greenlet_runner, self).__init__(desc)
        self.glet = greenlet(self.run)
        self.glet.switch()

    def __exit__(self, *args):
        super(greenlet_runner, self).__exit__(*args)
        self.glet.switch()

    def handle_result(self, exc_info):
        super(greenlet_runner, self).handle_result(exc_info)
        self.glet.switch(self.cases.pop())

    def run(self):
        suite = GreenSuite()
        unittest.TextTestRunner().run(suite)
