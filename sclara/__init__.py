import types


class App(object):
    cases = []
    stack = []
    runners = []

    def setup(self, func):
        return self.stack[-1].setup(func)

    def teardown(self, func):
        return self.stack[-1].teardown(func)

    @property
    def description(self):
        return self.runner.description

    @property
    def test(self):
        return self.runner.test

    @property
    def runner(self):
        return self.runners[-1]
default_app = App()


import dsl
from dsl.runner import greenlet_runner, delayed_runner


def description(*args):
    try:
        return default_app.description(*args)
    except IndexError:
        return dsl.description(*args)
def test(*args):
    try:
        return default_app.test(*args)
    except IndexError:
        return dsl.test(*args)
def setup(func):
    # nose finds this and tries to run it when setting up a test suite; hack
    # to stop that
    if not isinstance(func, types.FunctionType):
        return None
    return default_app.setup(func)
def teardown(func):
    # nose finds this and tries to run it when tearing down a test suite; hack
    # to stop that
    if not isinstance(func, types.FunctionType):
        return None
    return default_app.teardown(func)


__all__ = ['description', 'test', 'setup', 'teardown', 'delayed_runner',
    'greenlet_runner', 'default_app']
