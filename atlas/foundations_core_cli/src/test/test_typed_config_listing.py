

from foundations_spec import *
from foundations_contrib.utils import foundations_home

class TestTypeConfigListing(Spec):

    @let
    def config_type(self):
        return self.faker.name()
    
    @let
    def local_config_root(self):
        return f'config/{self.config_type}'

    @let
    def foundations_config_root(self):
        return f'{self.expanded_foundations_home}/config/{self.config_type}'

    mock_config_manager = let_patch_mock('foundations_contrib.global_state.config_manager')

    local_config_listing = let_mock()
    foundations_config_listing = let_mock()
    mock_listing_constructor = let_patch_mock_with_conditional_return('foundations_core_cli.config_listing.ConfigListing')

    config_name = let_mock()

    local_mock_config = let_mock()
    foundations_mock_config = let_mock()

    mock_expand_home = let_patch_mock_with_conditional_return('os.path.expanduser')

    @let
    def expanded_foundations_home(self):
        return self.faker.uri_path()

    @let
    def typed_listing(self):
        from foundations_core_cli.typed_config_listing import TypedConfigListing
        return TypedConfigListing(self.config_type)

    @let
    def mock_translate(self):
        return ConditionalReturn()

    translated_config = let_mock()

    @set_up
    def set_up(self):
        self.mock_expand_home.return_when(self.expanded_foundations_home, foundations_home())
        self.mock_listing_constructor.return_when(self.local_config_listing, self.local_config_root)
        self.mock_listing_constructor.return_when(self.foundations_config_listing, self.foundations_config_root)
        self.local_config_listing.config_path.return_value = None
        self.foundations_config_listing.config_path.return_value = None
        self.local_config_listing.config_data.return_value = None
        self.foundations_config_listing.config_data.return_value = None

        self.mock_translate.return_when(self.translated_config, self.foundations_mock_config)

    def test_config_path_returns_none_when_not_present(self):
        self.assertIsNone(self.typed_listing.config_path(self.config_name))

    def test_config_path_returns_config_path_when_present_in_local_listing(self):
        self.local_config_listing.config_path = ConditionalReturn()
        self.local_config_listing.config_path.return_when(self.local_mock_config, self.config_name)
        self.assertEqual(self.local_mock_config, self.typed_listing.config_path(self.config_name))

    def test_config_path_returns_config_path_when_present_in_foundations_listing(self):
        self.foundations_config_listing.config_path = ConditionalReturn()
        self.foundations_config_listing.config_path.return_when(self.foundations_mock_config, self.config_name)
        self.assertEqual(self.foundations_mock_config, self.typed_listing.config_path(self.config_name))

    def test_config_path_returns_local_config_path_when_present_in_both_listings(self):
        self.local_config_listing.config_path = ConditionalReturn()
        self.local_config_listing.config_path.return_when(self.local_mock_config, self.config_name)
        self.foundations_config_listing.config_path = ConditionalReturn()
        self.foundations_config_listing.config_path.return_when(self.foundations_mock_config, self.config_name)
        self.assertEqual(self.local_mock_config, self.typed_listing.config_path(self.config_name))

    def test_config_data_raises_error_when_not_present(self):
        with self.assertRaises(ValueError) as error_context:
            self.typed_listing.config_data(self.config_name)
        self.assertIn(f'No {self.config_type} config {self.config_name} found', error_context.exception.args[0])

    def test_config_data_returns_config_data_when_present_in_local_listing(self):
        self.local_config_listing.config_data = ConditionalReturn()
        self.local_config_listing.config_data.return_when(self.local_mock_config, self.config_name)
        self.assertEqual(self.local_mock_config, self.typed_listing.config_data(self.config_name))

    def test_config_data_returns_config_data_when_present_in_foundations_listing(self):
        self.foundations_config_listing.config_data = ConditionalReturn()
        self.foundations_config_listing.config_data.return_when(self.foundations_mock_config, self.config_name)
        self.assertEqual(self.foundations_mock_config, self.typed_listing.config_data(self.config_name))

    def test_config_data_returns_local_config_data_when_present_in_both_listings(self):
        self.local_config_listing.config_data = ConditionalReturn()
        self.local_config_listing.config_data.return_when(self.local_mock_config, self.config_name)
        self.foundations_config_listing.config_data = ConditionalReturn()
        self.foundations_config_listing.config_data.return_when(self.foundations_mock_config, self.config_name)
        self.assertEqual(self.local_mock_config, self.typed_listing.config_data(self.config_name))

    def test_update_config_manager_with_config_calls_update_with_specified_config(self):
        self.foundations_config_listing.config_data = ConditionalReturn()
        self.foundations_config_listing.config_data.return_when(self.foundations_mock_config, self.config_name)
        self.typed_listing.update_config_manager_with_config(self.config_name, self.mock_translate)
        self.mock_config_manager.config().update.assert_called_with(self.translated_config)

