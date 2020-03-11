
from foundations_spec import *
from foundations.job_parameters import load_parameters

class TestLoadJobParameters(Spec):
    
    mock_open = let_patch_mock_with_conditional_return('builtins.open')
    mock_log_param = let_patch_mock('foundations.job_parameters.log_param')

    def mock_parameters_list(self):
        return self.faker.words()

    def mock_parameters_generator(self):
        keys = self.mock_parameters_list()
        values = self.mock_parameters_list()
        return {key: value for key, value in zip(keys, values)}

    @let
    def mock_parameters(self):
        return self.mock_parameters_generator()

    @let
    def mock_nested_parameters(self):
        return {
            self.faker.word(): self.mock_parameters_list(),
            self.faker.word(): self.mock_parameters_generator(),
            self.faker.word(): self.faker.random_int(1, 100)
        }

    @let
    def serialized_mock_parameters(self):
        import json
        return json.dumps(self.mock_parameters)

    mock_file = let_mock()

    @set_up
    def set_up(self):
        self.mock_file.__enter__ = self._mock_file_enter
        self.mock_file.__exit__ = self._mock_exit
        self.mock_file.read.return_value = self.serialized_mock_parameters
        self.mock_open.return_when(self.mock_file, 'foundations_job_parameters.json', 'r')

    def test_can_load_json_parameters(self):
        self.assertEqual(self.mock_parameters, load_parameters())

    def test_is_accessible_globally(self):
        import foundations
        self.assertEqual(load_parameters, foundations.load_parameters)

    def test_returns_default_of_empty_dict_if_file_not_found(self):
        mock_open = self.patch('builtins.open')
        mock_open.side_effect = FileNotFoundError('beep')
        self.assertEqual({}, load_parameters())

    def test_returns_default_of_empty_dict_if_file_is_empty(self):
        self.mock_file.read.return_value = ''
        self.assertEqual({}, load_parameters())

    def test_raises_exception_if_file_is_not_valid_json(self):
        import json

        self.mock_file.read.return_value = self.faker.sentence()

        with self.assertRaises(json.JSONDecodeError):
            load_parameters()

    def test_logs_params_from_file(self):
        load_parameters()

        for param_key, param_value in self.mock_parameters.items():
            self.mock_log_param.assert_any_call(param_key, param_value)

    def test_logs_nested_params_from_file_after_flattening(self):
        import json
        from foundations.job_parameters import flatten_parameter_dictionary

        self.mock_file.read.return_value = json.dumps(self.mock_nested_parameters)

        load_parameters()

        for param_key, param_value in flatten_parameter_dictionary(self.mock_nested_parameters).items():
            self.mock_log_param.assert_any_call(param_key, param_value)

    def test_logs_nothing_if_log_parameters_false(self):
        import json
        from foundations.job_parameters import flatten_parameter_dictionary

        self.mock_file.read.return_value = json.dumps(self.mock_nested_parameters)

        load_parameters(log_parameters=False)

        self.mock_log_param.assert_not_called()

    def _mock_file_enter(self, *args, **kwargs):
        return self.mock_file

    def _mock_exit(self, *args, **kwargs):
        pass