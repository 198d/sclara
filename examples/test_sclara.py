import time

from sclara import simple_runner, greenlet_runner as runner


with runner() as (description, test):
    with description('sclara') as (setup, teardown):
        @setup
        def setup(context):
            context.foo = 'bar'
            context.baz = 'baz'

        with test('does not have access to inner setup context') as context:
            try:
                context.bar
            except AttributeError:
                pass

        with test('fails like a normal test'):
            assert False

        with description('with nested descriptions') as (setup, teardown):
            @setup
            def setup(context):
                context.bar = 'foo'
                context.baz = 'zab'

            with test('has access to inner setup context') as context:
                assert context.foo == 'bar'

            with test('has access to outer setup context') as context:
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


with runner() as (description, test):
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
