class ContextAware(object):
    def __init__(self, function):
        self._function = function
        self.__name__ = self._function.__name__
        self._stage_context = None

    def _set_context(self, stage_context):
        self._stage_context = stage_context
        stage_context.is_context_aware = True

    def __call__(self, *args, **kwargs):
        return self._function(self._stage_context, *args, **kwargs)

def context_aware(function, *args):
    if len(args) == 0:
        return ContextAware(function)
    else:
        return (ContextAware(function),) + args