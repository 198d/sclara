from sclara import test, description, setup, teardown


with description('Describing something interesting'):
    @setup
    def _setup(context):
        context.foo = 'foo'

    with test('that has a test at the top level') as context:
        assert context.foo == 'foo'

    with test('that fails'):
        assert False

    with description('that has bad setup'):
        @setup
        def _setup(context):
            raise Exception, 'bad setup'

        with test('fails'):
            assert True

    with description('that has bad teardown'):
        @teardown
        def _teardown(context):
            raise Exception, 'bad teardown'

        with test('fails'):
            assert True

    with description('that has many levels of interest'):
        @setup
        def _setup(context):
            context.bar = 'bar'

        with test('and then testing it') as context:
            assert context.bar == 'bar'
        with test('and testing something else') as context:
            assert context.foo == 'foo'
