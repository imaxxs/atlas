
from unittest import skip
from mock import call, Mock

from foundations_spec.helpers.callback import Callback
from foundations_spec.helpers.let import let

class set_up(Callback):
    pass 

class set_up_class(Callback):
    pass

class tear_down(Callback):
    pass 

class tear_down_class(Callback):
    pass

class let_now(let):
    pass

def let_mock():
    
    def _callback(self):
        return Mock()
    
    return let(_callback)

def let_patch_mock(name, *args, **kwargs):
    def _callback(self):
        return self.patch(name, *args, **kwargs)
    
    return let_now(_callback)

def let_patch_mock_with_conditional_return(name):
    def _callback(self):
        from foundations_spec.helpers.conditional_return import ConditionalReturn
        return self.patch(name, ConditionalReturn())
    
    return let_now(_callback)


def let_patch_instance(name):

    def _callback(self):
        mock_klass = self.patch(name)
        mock_instance = Mock()
        mock_klass.return_value = mock_instance

        return mock_instance
    
    return let_now(_callback)