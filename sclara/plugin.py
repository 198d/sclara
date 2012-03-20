import unittest

import nose
from nose.selector import TestAddress

from sclara.builder import generate_test_cases
from sclara.dsl import test
from sclara.dsl.runner import runner


class nose_test(test):
    def __exit__(self, type_, value, traceback):
        teardown_exc_info = self._teardown()
        if self.setup_exc_info:
            raise self.setup_exc_info[0], self.setup_exc_info[1], \
                self.setup_exc_info[2]
        elif teardown_exc_info:
            raise teardown_exc_info[0], teardown_exc_info[1], \
                teardown_exc_info[2]
        return False


class nose_runner(runner):
    def __init__(self):
        super(nose_runner, self).__init__()
        self.test = nose_test


class Nose(nose.plugins.Plugin):
    enabled=True
    name='nose-sclara'

    def options(self, parser, env):
        pass

    def configure(self, options, conf):
        pass

    def begin(self):
        self.runner = nose_runner()
        self.runner.__enter__()

    def finalize(self, result):
        self.runner.__exit__()

    def loadTestsFromName(self, name, module):
        addr = TestAddress(name, module)
        if addr.filename and addr.module:
            return list(generate_test_cases(addr.filename))


if __name__ == '__main__':
    nose.main(plugins=[Nose()])
