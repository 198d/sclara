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


from dsl.runner import greenlet_runner, delayed_runner

def description(*args):
    return default_app.description(*args)
def test(*args):
    return default_app.test(*args)
def setup(func):
    return default_app.setup(func)
def teardown(func):
    return default_app.teardown(func)


__all__ = ['description', 'test', 'setup', 'teardown', 'delayed_runner',
    'greenlet_runner', 'default_app']
