"""
Copyright (C) DeepLearning Financial Technologies Inc. - All Rights Reserved
Unauthorized copying, distribution, reproduction, publication, use of this file, via any medium is strictly prohibited
Proprietary and confidential
Written by Thomas Rogers <t.rogers@dessa.com>, 06 2018
"""

from foundations_spec import *

from foundations_orbit.data_contract import DataContract

class TestDataContract(Spec):

    @let
    def contract_name(self):
        return self.faker.word()

    def test_can_import_data_contract_from_foundations_orbit_top_level(self):
        import foundations_orbit
        self.assertEqual(DataContract, foundations_orbit.DataContract)

    def test_data_contract_takes_contract_name(self):
        try:
            DataContract(self.contract_name)
        except TypeError as ex:
            raise AssertionError('data contract class takes contract name as argument') from ex

    def test_data_contract_has_options_with_default_max_bins_50(self):
        self._test_data_contract_has_default_option('max_bins', 50)

    def test_data_contract_has_options_with_default_check_schema_True(self):
        self._test_data_contract_has_default_option('check_schema', True)

    def test_data_contract_has_options_with_default_check_row_count_False(self):
        self._test_data_contract_has_default_option('check_row_count', False)

    def _test_data_contract_has_default_option(self, option_name, default_value):
        contract = DataContract(self.contract_name)
        self.assertEqual(default_value, getattr(contract.options, option_name))