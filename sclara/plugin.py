import unittest

import nose
from nose.selector import TestAddress

from sclara.builder import generate_test_cases
from sclara.runner import test_runner


class nose_runner(test_runner):
    def handle_result(self, exc_info):
        type_, value, traceback = exc_info
        if type_:
            raise type_, value, traceback


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
