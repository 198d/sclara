import inspect
import unittest
import sys

from sclara import default_app


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
        self.current_context = default_app.stack[-1]

    def __enter__(self):
        execution_context = self.ExecutionContext()
        for description in default_app.stack:
            if description.setup_func:
                description.setup_func(execution_context)
        self.execution_context = execution_context
        return self.execution_context

    def __exit__(self, type_, value, traceback):
        try:
            for description in default_app.stack:
                if description.teardown_func:
                    description.teardown_func(self.execution_context)
        except:
            type_, value, traceback = sys.exc_info()
        self._clear_context_from_stack()

        prefix = " ".join([c.desc for c in default_app.stack])
        test_statement = "{} {}".format(prefix, self.desc)
        if type_:
            def test_method(self):
                raise type_, value, traceback
        else:
            def test_method(self):
                pass
        test_method.__name__ = test_statement
        test_method.__doc__ = test_statement

        test_case_class = type("TestCase", (unittest.TestCase,),
            {test_method.__name__: test_method})
        test_case = test_case_class(test_method.__name__)

        default_app.cases.append(test_case)

        return True

    def _clear_context_from_stack(self):
        stack = inspect.stack()
        for level in stack:
            frame = level[0]
            for k, v in frame.f_locals.items():
                if isinstance(v, self.ExecutionContext):
                    del frame.f_locals[k]
