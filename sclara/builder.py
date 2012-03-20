import ast
import itertools
import re
import unittest
from copy import deepcopy

class HelperMixin(object):
    def test_statement(self, node):
        return " ".join([n.context_expr.args[0].s for n in itertools.chain(
            self.desc_stack, [node])])

    def is_description(self, node):
        return node.context_expr.func.id == 'description'

    def is_test(self, node):
        return node.context_expr.func.id == 'test'


class TestCaseCollector(ast.NodeVisitor, HelperMixin):
    desc_stack = []
    test_statements = []

    def visit_With(self, node):
        if self.is_description(node):
            self.desc_stack.append(node)
            self.generic_visit(node)
            self.desc_stack.pop()
        elif self.is_test(node):
            self.test_statements.append(self.test_statement(node))


class TestMethodBuilder(ast.NodeTransformer, HelperMixin):
    desc_stack = []

    def __init__(self, target_statement):
        super(TestMethodBuilder, self).__init__()
        self.target_statement = target_statement

    def visit_Module(self, node):
        self.generic_visit(node)

        body = ast.FunctionDef(name=self.target_statement, args=ast.arguments(
            args=[ast.Name(id='self', ctx=ast.Param(), lineno=0, col_offset=0)],
            vararg=None, kwarg=None, defaults=[]), body=node.body,
            decorator_list=[], lineno=0, col_offset=0)
        node.body = [body]

        return node

    def visit_With(self, node):

        if self.is_description(node):
            self.desc_stack.append(node)
            self.generic_visit(node)
            if not node.body:
                return None
            self.desc_stack.pop()
        elif self.is_test(node):
            if self.target_statement == self.test_statement(node):
                return node
            return None

        return node


def generate_test_cases(filename):
    with file(filename) as f:
        tree = ast.parse(f.read(), filename)

    walker = TestCaseCollector()
    walker.visit(tree)

    for statement in walker.test_statements:
        tree_copy = deepcopy(tree)

        builder = TestMethodBuilder(statement)
        builder.visit(tree_copy)

        exec_locals = {}
        exec compile(tree_copy, filename, 'exec') in exec_locals

        test_case_class = type('TestCase', (unittest.TestCase,),
            {statement: exec_locals[statement]})
        yield test_case_class(statement)
