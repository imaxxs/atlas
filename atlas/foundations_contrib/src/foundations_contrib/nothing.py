

class Nothing(object):

    def map(self, function):
        return Nothing()

    def is_present(self):
        return False

    def get(self):
        raise ValueError('Tried #get on Nothing')

    def get_or_else(self, value):
        return value

    def fallback(self, callback):
        from foundations_contrib.option import Option
        return Option(callback())

    def __eq__(self, other):
        return isinstance(other, Nothing)
