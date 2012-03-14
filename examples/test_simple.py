from sclara import test, description


with description('Describing something interesting') as (setup, teardown):
    @setup
    def setup(context):
        context.foo = 'foo'

    with test('that has a test at the top level') as context:
        assert context.foo == 'foo'

    with description('that has many levels of interest') as (setup, teardown):
        @setup
        def setup(context):
            context.bar = 'bar'

        with test('and then testing it') as context:
            assert context.bar == 'bar'
        with test('and testing something else') as context:
            assert context.foo == 'foo'
