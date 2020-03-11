

class TestCallback(object):

    def _callback(self, args, kwargs):
        from uuid import uuid4

        self._called_callback = True
        self._callback_args = args
        self._callback_kwargs = kwargs

        if not hasattr(self, '_callback_result') or self._callback_result is None:
            self._callback_result = uuid4()
        return self._callback_result
