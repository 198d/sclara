import inspect
import sys


class expect(object):
    def __new__(cls, subject, *args):
        if isinstance(subject, bool):
            assert subject, 'Expected {0} to be True'.format(subject)
        return object.__new__(cls, subject, *args)

    def __init__(self, subject, *args):
        self.subject = subject
        self.args = args

    def __eq__(self, other):
        assert self.subject == other, \
            'Expected {0} to be equal to {1}'.format(self.subject, other)

    def __ne__(self, other):
        assert self.subject != other, \
            'Expected {0} to not equal {1}'.format(self.subject, other)

    def __lt__(self, other):
        assert self.subject < other, \
            'Expected {0} to be less than {1}'.format(self.subject, other)

    def __gt__(self, other):
        assert self.subject > other, \
            'Expected {0} to be greather than {1}'.format(self.subject, other)

    def __le__(self, other):
        assert self.subject <= other, \
            'Expected {0} to be less than or equal to {1}'.format(
                self.subject, other)

    def __ge__(self, other):
        assert self.subject >= other, \
            'Expected {0} to be greater than or equal to {1}'.format(
                self.subject, other)

    def contains(self, item):
        assert item in self.subject, \
            "Expected {0} to contain {1}".format(self.subject, item)

    def raises(self, exception):
        try:
            self.subject(*self.args)
        except:
            type_, _, _ = sys.exc_info()
            assert exception == type_, \
                'Expected {0} to raise {1}, however, {2} was raised'.format(
                    self.subject, exception, type_)
