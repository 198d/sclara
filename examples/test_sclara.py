import time

from sclara import description, test, greenlet_runner, delayed_runner


with delayed_runner('delayed runner for'):
    with description('sclara'):
        def setup(context):
            context.foo = 'bar'
            context.baz = 'baz'

        with test('does not have access to inner setup context') as context:
            try:
                context.bar
            except AttributeError:
                pass
            else:
                assert False

        with test('fails like a normal test'):
            assert False

        with description('during setup'):
            def setup(context):
                raise Exception, 'failed setup'

            with test('fails well'):
                assert True

        with description('during teardown'):
            def teardown(context):
                raise Exception, 'failed teardown'

            with test('fails well'):
                assert True

        with description('with nested descriptions'):
            def setup(context):
                context.bar = 'foo'
                context.baz = 'zab'

            with test('has access to outer setup context') as context:
                assert context.foo == 'bar'

            with test('has access to inner setup context') as context:
                assert context.bar == 'foo'

            with test('overrides outer setup context with inner context') as context:
                assert context.baz == 'zab'

            with test('fails if context object isn\'t bound'):
                raised = False
                try:
                    context.baz
                except NameError:
                    raised = True
                assert raised


with greenlet_runner('greenlet runner with'):
    with description('sloooowwwww tests'):
        with test('print dots as they happen'):
            time.sleep(1)
            assert True
        with test('print failures as they happen, too'):
            time.sleep(2)
            assert False
        with test('print more dots'):
            time.sleep(3)
            assert True
