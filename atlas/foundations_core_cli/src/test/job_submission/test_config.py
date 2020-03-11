
from foundations_spec import *

from foundations_core_cli.job_submission.config import load

class TestJobSubmissionConfig(Spec):
    
    mock_config_listing_klass = let_patch_mock_with_conditional_return('foundations_core_cli.typed_config_listing.TypedConfigListing')
    exit_mock = let_patch_mock('sys.exit')
    print_mock = let_patch_mock('builtins.print')

    @let
    def mock_config_listing(self):
        mock = ConditionalReturn()
        mock.config_path.return_when(None, self.config_name)
        mock.update_config_manager_with_config = Mock()
        return mock
    
    @let
    def config_name(self):
        return self.faker.name()

    @set_up
    def set_up(self):
        self.mock_config_listing_klass.return_when(self.mock_config_listing, 'submission')

    def test_exits_when_config_missing(self):
        load(self.config_name)
        self.exit_mock.assert_called_with(1)

    def test_prints_warning_message_when_config_missing(self):
        load(self.config_name)
        self.print_mock.assert_called_with(f"Could not find submission configuration with name: `{self.config_name}`")

    def test_does_not_exit_when_config_present(self):
        self._set_up_config()
        load(self.config_name)
        self.exit_mock.assert_not_called()

    def test_does_not_print_error_when_config_present(self):
        self._set_up_config()
        load(self.config_name)
        self.print_mock.assert_not_called()

    def test_loads_config_into_config_manager_when_config_present(self):
        from foundations_local_docker_scheduler_plugin.config.scheduler import translate

        self._set_up_config()
        load(self.config_name)
        self.mock_config_listing.update_config_manager_with_config.assert_called_with(self.config_name, translate)

    def _set_up_config(self):
        self.mock_config_listing.config_path.clear()
        self.mock_config_listing.config_path.return_when(self.faker.uri_path(), self.config_name)

