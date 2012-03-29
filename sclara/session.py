import types

class Session(list):
    @property
    def description(self):
        return " ".join([context.desc for tag, context in self])

    def push(self, context, tag=None):
        if not tag:
            tag = context.__class__.__name__
        self.append((tag, context))

    def closest(self, tag):
        for frame in reversed(self):
            if tag == frame[0]:
                return frame[1]

    def all(self, tag):
        for frame in self:
            if tag == frame[0]:
                yield frame[1]
session = Session()
