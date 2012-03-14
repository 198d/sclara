from sclara import test, description, setup, teardown


with description('Describing something interesting'):
    @setup
    def _setup(context):
        context.foo = 'foo'

    with test('that has a test at the top level') as context:
        assert context.foo == 'foo'

    with description('that has many levels of interest'):
        @setup
        def _setup(context):
            context.bar = 'bar'

        with test('and then testing it') as context:
            assert context.bar == 'bar'
        with test('and testing something else') as context:
            assert context.foo == 'foo'
