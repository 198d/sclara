import ast
import itertools
import re


class AbstractSuiteBuilder(ast.NodeTransformer):
    desc_stack = []

    def __init__(self, pattern):
        super(AbstractSuiteBuilder, self).__init__()
        self.match_re = re.compile(pattern)

    def visit_With(self, node):
        def test_statement(node):
            return " ".join([n.context_expr.args[0].s for n in itertools.chain(
                self.desc_stack, [node])])
        def is_description(node):
            return node.context_expr.func.id == 'description'
        def is_test(node):
            return node.context_expr.func.id == 'test'

        if is_description(node):
            self.desc_stack.append(node)
            self.generic_visit(node)
            if not node.body:
                return None
            self.desc_stack.pop()
        elif is_test(node):
            if self.match_re.search(test_statement(node)):
                return node
            return None

        return node


if __name__ == '__main__':
    import sys
    test = sys.argv[1]
    pattern = sys.argv[2]

    with file(test) as f:
        tree = ast.parse(f.read(), test)
    builder = AbstractSuiteBuilder(r'{}'.format(pattern))
    builder.visit(tree)

    from sclara import greenlet_runner as runner
    code = compile(tree, test, 'exec')
    with runner():
        exec(code)
