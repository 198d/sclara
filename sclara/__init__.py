import types


class App(object):
    stack = []
    runners = []

    def setup(self, func):
        return self.stack[-1].setup(func)

    def teardown(self, func):
        return self.stack[-1].teardown(func)

    def deliver_result(self, exc_info):
        self.runner.handle_result(exc_info)

    @property
    def test_statement(self):
        return " ".join([s.desc for s in self.stack])

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


from dsl import test, description, greenlet_runner, delayed_runner


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
