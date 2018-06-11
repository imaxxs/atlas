"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

class LogManager(object):

    def __init__(self):
        self._loggers = None

    def get_logger(self, name):
        if self._loggers is None:
            self._load()

        if not name in self._loggers:
            self._add_logger(name)

        return self._loggers[name]

    def _load(self):
        from vcat.global_state import config_manager
        from logging import basicConfig
        from logging import getLevelName
        from sys import stdout

        log_level = config_manager.config().get('log_level', 'INFO')
        log_level = getLevelName(log_level)
        basicConfig(stream=stdout, level=log_level)

        self._loggers = {}

    def _add_logger(self, name):
        from logging import getLogger
        self._loggers[name] = getLogger(name)
