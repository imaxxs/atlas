"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class ModuleManager(object):

    def __init__(self):
        self._module_listing = []

    def append_module(self, module):
        self._module_listing.append(module)

    def module_directories_and_names(self):
        import os

        for module in self._module_listing:
            module_directory = os.path.dirname(module.__file__)
            yield module.__name__, module_directory
