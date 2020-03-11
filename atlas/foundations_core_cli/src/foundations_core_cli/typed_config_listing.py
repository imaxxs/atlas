
class TypedConfigListing(object):
    
    def __init__(self, config_type):
        from foundations_core_cli.config_listing import ConfigListing
        from foundations_contrib.utils import foundations_home
        import os.path

        self._config_type = config_type
        self._local_listing = ConfigListing(f'config/{self._config_type}')
        self._foundations_listing = ConfigListing(f'{os.path.expanduser(foundations_home())}/config/{self._config_type}')

    def config_path(self, name):
        return self._local_listing.config_path(name) or self._foundations_listing.config_path(name)

    def config_data(self, name):
        result = self._local_listing.config_data(name) or self._foundations_listing.config_data(name)
        if result is None:
            raise ValueError(f'No {self._config_type} config {name} found')
        return result

    def update_config_manager_with_config(self, name, config_translate):
        from foundations_contrib.global_state import config_manager

        config = self.config_data(name)
        translated_config = config_translate(config)
        config_manager.config().update(translated_config)
