import inspect
import unittest
import sys

from sclara import default_app


__test__ = False


class description(object):
    setup_func = None
    teardown_func = None

    def __init__(self, desc):
        self.desc = desc

    def __enter__(self):
        default_app.stack.append(self)
        return self.setup, self.teardown

    def __exit__(self, *args):
        default_app.stack.pop()
        return False

    def setup(self, func):
        self.setup_func = func
        return func

    def teardown(self, func):
        self.teardown_func = func
        return func


class test(object):
    class ExecutionContext(object):
        pass

    def __init__(self, desc):
        self.desc = desc
        self.setup_exc_info = None
        self.teardown_exc_info = None
        self.execution_context = self.ExecutionContext()

    def __enter__(self):
        default_app.stack.append(self)
        return self._setup()

    def __exit__(self, type_, value, traceback):
        self._teardown()
        if self.setup_exc_info:
            type_, value, traceback = self.setup_exc_info
        elif self.teardown_exc_info:
            type_, value, traceback = self.teardown_exc_info

        default_app.deliver_result((type_, value, traceback))
        default_app.stack.pop()
        return True

    def _setup(self):
        try:
            for description in default_app.stack:
                if getattr(description, 'setup_func', None):
                    description.setup_func(self.execution_context)
        except:
            self.setup_exc_info = sys.exc_info()
        return self.execution_context

    def _teardown(self):
        self._clear_context_from_stack()
        try:
            for description in default_app.stack:
                if getattr(description, 'teardown_func', None):
                    description.teardown_func(self.execution_context)
        except:
            self.teardown_exc_info = sys.exc_info()

    def _clear_context_from_stack(self):
        stack = inspect.stack()
        for level in stack:
            frame = level[0]
            for k, v in frame.f_locals.items():
                if isinstance(v, self.ExecutionContext):
                    del frame.f_locals[k]
