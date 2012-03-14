from pprint import pprint

import dsl


class App(object):
    cases = []
    stack = []
    description = dsl.description
    test = dsl.test


default_app = App()


def description(*args):
    return default_app.description(*args)
def test(*args):
    return default_app.test(*args)


simple_runner = dsl.simple_runner
greenlet_runner = dsl.greenlet_runner


__all__ = ['description', 'test', 'simple_runner', 'greenlet_runner',
    'default_app']
