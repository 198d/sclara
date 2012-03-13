import inspect
import unittest
import sys
import types

from greenlet import greenlet


context_stack = []
cases = []


class GreenSuite(unittest.TestSuite):
    def __iter__(self):
        while True:
            case = greenlet.getcurrent().parent.switch()
            if case:
                yield case
            else:
                raise StopIteration


class simple_runner(object):
    def __enter__(self):
        return description, test

    def __exit__(self, *args):
        global cases
        suite = unittest.TestSuite(cases)
        unittest.TextTestRunner().run(suite)
        cases = []


class greenlet_runner(object):
    def __enter__(self):
        green_test.glet = greenlet(self.runner)
        green_test.glet.switch()
        return description, green_test

    def __exit__(self, *args):
        green_test.glet.switch()

    def runner(self):
        suite = GreenSuite()
        unittest.TextTestRunner().run(suite)


class description(object):
    setup_func = None
    teardown_func = None

    def __init__(self, desc):
        self.desc = desc

    def __enter__(self):
        context_stack.append(self)
        return self.setup, self.teardown

    def __exit__(self, *args):
        context_stack.pop()
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
        self.current_context = context_stack[-1]

    def __enter__(self):
        execution_context = self.ExecutionContext()
        for description in context_stack:
            if description.setup_func:
                description.setup_func(execution_context)
        self.execution_context = execution_context
        return self.execution_context

    def __exit__(self, type_, value, traceback):
        try:
            for description in context_stack:
                if description.teardown_func:
                    description.teardown_func(self.execution_context)
        except:
            type_, value, traceback = sys.exc_info()
        self._clear_context_from_stack()

        prefix = " ".join([c.desc for c in context_stack])
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

        cases.append(test_case)

        return True

    def _clear_context_from_stack(self):
        stack = inspect.stack()
        for level in stack:
            frame = level[0]
            for k, v in frame.f_locals.items():
                if isinstance(v, self.ExecutionContext):
                    del frame.f_locals[k]


class green_test(test):
    glet = None

    def __exit__(self, *args):
        super(green_test, self).__exit__(*args)
        self.glet.switch(cases.pop())
        return True
