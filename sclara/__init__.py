from pprint import pprint

import dsl


class App(object):
    cases = []
    stack = []
    description = dsl.description
    test = dsl.test

    def setup(self, func):
        return self.stack[-1].setup(func)

    def teardown(self, func):
        return self.stack[-1].teardown(func)


default_app = App()


def description(*args):
    return default_app.description(*args)
def test(*args):
    return default_app.test(*args)
def setup(func):
    return default_app.setup(func)
def teardown(func):
    return default_app.teardown(func)


simple_runner = dsl.simple_runner
greenlet_runner = dsl.greenlet_runner


__all__ = ['description', 'test', 'setup', 'teardown', 'simple_runner',
    'greenlet_runner', 'default_app']
