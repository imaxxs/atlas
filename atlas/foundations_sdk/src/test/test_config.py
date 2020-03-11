
from foundations_spec import *


class TestConfig(Spec):

    @let
    def path(self):
        return self.faker.uri_path()

    @let
    def environment_name(self):
        return self.faker.name()

    @let
    def non_existent_environment_name(self):
        return self.faker.name()

    mock_environment_fetcher = let_patch_instance('foundations_core_cli.environment_fetcher.EnvironmentFetcher')
    mock_config_manager = let_patch_mock('foundations_contrib.global_state.config_manager')

    @set_up
    def set_up(self):
        self.mock_environment_fetcher.find_environment = ConditionalReturn()
        self.mock_environment_fetcher.find_environment.return_when([self.path], self.environment_name)
        self.mock_environment_fetcher.find_environment.return_when([], self.non_existent_environment_name)
    
    def test_adds_simple_configuration_to_config_manager(self):
        from foundations.config import set_environment        

        set_environment(self.environment_name)
        self.mock_config_manager.add_simple_config_path.assert_called_with(self.path)
    
    def test_raises_error_if_non_existent_environment_provided(self):
        from foundations.config import set_environment        

        with self.assertRaises(ValueError) as error_context:
            set_environment(self.non_existent_environment_name)

        error_message = 'No environment {} found, please set a valid deployment environment with foundations.set_environment'.format(self.non_existent_environment_name)
        self.assertIn(error_message, error_context.exception.args)

    def test_set_environment_is_globally_accesible(self):
        import foundations.config
        import foundations

        self.assertEqual(foundations.set_environment, foundations.config.set_environment)