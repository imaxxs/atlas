
from mock import Mock

class ConditionalReturn(Mock):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._returns = []

    def __call__(self, *args, **kwargs):
        expected_key = (args, kwargs)
        for key, value in self._returns:
            if key == expected_key:
                super().__call__(*args, **kwargs)
                return value
        
        error_message_called_with = 'Mock called with unexpected arguments ({}, {})'.format(args, kwargs)
        error_message_correct_value = '\nSupported arguments:'
        for (return_args, return_kwargs), _ in self._returns:
            error_message_correct_value += '\n ({}, {})'.format(return_args, return_kwargs)
        raise AssertionError(error_message_called_with + error_message_correct_value)

    def return_when(self, value_to_be_returned_by_condition, *args, **kwargs):
        key = (args, kwargs)
        self._returns.append((key, value_to_be_returned_by_condition))

    def clear(self):
        self._returns = []