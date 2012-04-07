import time

from sclara import description, test, expect, greenlet_runner, \
    delayed_runner


with delayed_runner('delayed runner for'):
    with description('sclara'):
        def setup(context):
            context.foo = 'bar'
            context.baz = 'baz'

        with test('does not have access to inner setup context') as context:
            expect(lambda: context.bar).raises(AttributeError)

        with test('fails like a normal test'):
            expect(False)

        with test('expects dictionary pressence'):
            expect({'key': 'value'}).contains('key')

        with test('fails dictionary absence'):
            expect({'yek': 'value'}).contains('key')

        with description('during setup'):
            def setup(context):
                raise Exception, 'failed setup'

            with test('fails well'):
                expect(False)

        with description('during teardown'):
            def teardown(context):
                raise Exception, 'failed teardown'

            with test('fails well'):
                expect(False)

        with description('with nested descriptions'):
            def setup(context):
                context.bar = 'foo'
                context.baz = 'zab'

            with test('has access to outer setup context') as context:
                expect(context.foo) == 'bar'

            with test('has access to inner setup context') as context:
                expect(context.bar) == 'foo'

            with test('overrides outer setup context with inner context') as context:
                expect(context.baz) == 'zab'

            with test('fails if context object isn\'t bound'):
                expect(lambda: context.bar).raises(NameError)


with greenlet_runner('greenlet runner with'):
    with description('sloooowwwww tests'):
        with test('print dots as they happen'):
            time.sleep(1)
            expect(True)
        with test('print failures as they happen, too'):
            time.sleep(2)
            expect(False)
        with test('print more dots'):
            time.sleep(3)
            expect(True)
