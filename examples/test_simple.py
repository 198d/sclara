from sclara import test, description


with description('Describing something interesting'):
    def setup(context):
        context.foo = 'foo'

    with test('that has a test at the top level') as context:
        assert context.foo == 'foo'

    with test('that fails'):
        assert False

    with description('that has bad setup'):
        def setup(context):
            raise Exception, 'bad setup'

        with test('fails'):
            assert True

    with description('that has bad teardown'):
        def teardown(context):
            raise Exception, 'bad teardown'

        with test('fails'):
            assert False

    with description('that has many levels of interest'):
        def setup(context):
            context.bar = 'bar'

        with test('and then testing it') as context:
            assert context.bar == 'bar'
        with test('and testing something else') as context:
            assert context.foo == 'foo'
