

class LetNowMixin(object):

    @classmethod
    def _collect_let_nows(klass):
        from foundations_spec.helpers import let_now
        from foundations_spec.helpers.let_mixin import LetMixin

        if getattr(klass, '_let_nows', None) is None:
            klass._let_nows = {}

        for function_name, _, function in LetMixin._klass_attributes(klass):
            if isinstance(function, let_now):
                klass._let_nows[function_name] = function

    def _setup_let_nows(self):
        for let_name in self._let_nows:
            getattr(self, let_name)
