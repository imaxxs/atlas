
from foundations_spec import *
from foundations_contrib.log_manager import LogManager
import logging

class TestLogManager(Spec):

    @let
    def config_manager(self):
        from foundations_contrib.config_manager import ConfigManager
        return ConfigManager()

    @let
    def log_manager(self):
        return LogManager(self.config_manager)
        
    @let
    def result_logger(self):
        return self.log_manager.get_logger('namespaced_log_levels')

    @let
    def root_logger(self):
        return logging.getLogger()

    @let
    def console_log_handler(self):
        return self.root_logger.handlers[0]
  
    @let
    def file_log_handler(self):
        return self.root_logger.handlers[1]

    @let
    def file_log_path(self):
        import os
        import os.path

        FOUNDATIONS_HOME = os.getenv('FOUNDATIONS_HOME', '~/.foundations')
        if os.getenv('RUNNING_ON_CI'):
            return os.path.expanduser(f'{FOUNDATIONS_HOME}logs/system.log')
        return os.path.expanduser(f'{FOUNDATIONS_HOME}/logs/system.log')

    def test_root_logger_has_no_level_set(self):
        self._setup_logger()
        self.assertEqual(logging.NOTSET, self.root_logger.level)

    def test_logger_return_logging_type(self):
        self.assertTrue(isinstance(self.result_logger, logging.Logger))

    def test_logger_returns_log_level_info(self):
        self.assertEqual(logging.INFO, self.console_log_handler.level)

    def test_logger_return_log_level_override(self):
        self.config_manager['log_level'] = 'DEBUG'
        self._setup_logger()
        self.assertEqual(logging.DEBUG, self.console_log_handler.level)

    def test_logger_return_namespace_override(self):
        self.config_manager['namespaced_log_levels'] = {'a': 'DEBUG'}
        result_logger = self.log_manager.get_logger('a')
        self.assertEqual(logging.DEBUG, result_logger.level)

    def test_logger_return_namespace_override_matches_with_longer_value(self):
        self.config_manager['namespaced_log_levels'] = {'foundations': 'DEBUG'}
        result_logger = self.log_manager.get_logger('foundations_contrib.config_manager')
        self.assertEqual(logging.DEBUG, result_logger.level)
    
    def test_logger_return_namespace_override_matches_with_longest_match(self):
        self.config_manager['namespaced_log_levels'] = {'foundations': 'DEBUG', 'foundations_contrib.config_manager': 'ERROR'}
        result_logger = self.log_manager.get_logger('foundations_contrib.config_manager')
        self.assertEqual(logging.ERROR, result_logger.level)

    def test_logger_return_when_clears_default_handlers(self):
        self.log_manager.get_logger('foundations_contrib.config_manager')
        self.assertEqual(2, len(self.root_logger.handlers))

    def test_logger_return_when_clears_default_handlers(self):
        self.log_manager.get_logger('foundations_contrib.config_manager')
        self.assertEqual(2, len(self.root_logger.handlers))

    def test_console_log_handler_return_format(self):
        self.config_manager['log_level'] = 'DEBUG'
        self._setup_logger()
        formatter = self.console_log_handler.formatter
        self.assertEqual('%(asctime)s - %(name)s - %(levelname)s - %(message)s', formatter._fmt)

    def test_console_log_handler_return_stdout(self):
        from sys import stdout

        self.log_manager.get_logger('foundations_contrib.config_manager')
        self.assertEqual(stdout, self.console_log_handler.stream)

    def test_file_log_handler_return_format(self):
        self.config_manager['log_level'] = 'DEBUG'
        self._setup_logger()
        formatter = self.file_log_handler.formatter
        self.assertEqual('%(asctime)s - %(name)s - %(levelname)s - %(message)s', formatter._fmt)

    def test_file_log_handler_log_level_is_debug(self):
        self.log_manager.get_logger('foundations_contrib.config_manager')
        self.assertEqual(logging.DEBUG, self.file_log_handler.level)

    def test_file_log_handler_return_system_log(self):
        from sys import stdout

        self.log_manager.get_logger('foundations_contrib.config_manager')
        self.assertEqual(self.file_log_path, self.file_log_handler.baseFilename)

    def test_logger_return_cached_logger(self):
        first_logger = self.log_manager.get_logger('namespaced_log_levels')
        second_logger = self.log_manager.get_logger('namespaced_log_levels')
        self.assertEqual(id(first_logger), id(second_logger))
    
    def test_logger_return_different_loggers(self):
        first_logger = self.log_manager.get_logger('namespaced_log_levels')
        second_logger = self.log_manager.get_logger('namespaced_log_levels_two')
        self.assertNotEqual(first_logger, second_logger)

    def test_foundations_not_running_warning_printed_false_by_default(self):
        self.assertFalse(self.log_manager.foundations_not_running_warning_printed())

    def test_foundations_not_running_warning_printed_true_after_flag_set(self):
        self.log_manager.set_foundations_not_running_warning_printed()
        self.assertTrue(self.log_manager.foundations_not_running_warning_printed())

    def test_foundations_not_running_warning_printed_false_after_flag_reset(self):
        self.log_manager.set_foundations_not_running_warning_printed()
        self.log_manager.set_foundations_not_running_warning_printed(False)
        self.assertFalse(self.log_manager.foundations_not_running_warning_printed())

    def _setup_logger(self):
        self.log_manager.get_logger('test')