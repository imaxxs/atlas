"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class ContextAware(object):
    def __init__(self, function):
        self._function = function
        self.__name__ = self._function.__name__
        self._stage_context = None

    def set_context(self, stage_context):
        self._stage_context = stage_context
        stage_context.is_context_aware = True

    def __call__(self, *args, **kwargs):
        return self._function(self._stage_context, *args, **kwargs)

def context_aware(function, *args):
    if len(args) == 0:
        return ContextAware(function)
    else:
        return (ContextAware(function),) + args
