
from foundations_spec import *
from acceptance.mixins.run_local_job import RunLocalJob
class TestCanLoadParameters(Spec, RunLocalJob):

    @let
    def job_parameters(self):
        import json
        with open(self.script_directory + '/foundations_job_parameters.json', 'r') as file:
            return json.load(file)

    @let
    def project_name(self):
        return self.faker.word().lower()

    @let
    def script_directory(self):
        return 'acceptance/fixtures/script_parameters'

    @let
    def script_directory_no_parameters(self):
        return 'acceptance/fixtures/script_parameters_no_parameters'

    @let
    def deployable_script_directory(self):
        return 'acceptance/fixtures/deployable_script_parameters'

    @let
    def deployable_script_directory_no_parameters(self):
        return 'acceptance/fixtures/deployable_script_parameters_no_parameters'

    @let
    def script_directory_empty_params(self):
        return 'acceptance/fixtures/script_parameters_empty_params'

    @let
    def deployable_script_directory_empty_params(self):
        return 'acceptance/fixtures/deployable_script_parameters_empty_params'

    @set_up_class
    def set_up_class(klass):
        pass

    def test_can_load_parameters_within_python(self):
        self._test_can_load_parameters_within_python(self.script_directory, self.job_parameters, check_for_warning=True)

    @quarantine
    def test_can_load_parameters_within_foundations_submit(self):
        self._test_can_load_parameters_within_foundations_submit(self.deployable_script_directory, self.job_parameters)

    def test_can_load_parameters_as_empty_dict_within_python_empty_params(self):
        self._test_can_load_parameters_within_python(self.script_directory_empty_params, {})

    @quarantine
    def test_can_load_parameters_as_empty_dict_within_foundations_submit_empty_params(self):
        self._test_can_load_parameters_within_foundations_submit(self.deployable_script_directory_empty_params, {})

    @quarantine
    def test_can_load_default_parameters_within_foundations_submit_when_parameters_json_not_found(self):
        self._test_can_load_parameters_within_foundations_submit(self.deployable_script_directory_no_parameters, {})

    def test_can_load_default_parameters_within_python_when_parameters_json_not_found(self):
        self._test_can_load_parameters_within_python(self.script_directory_no_parameters, {})

    def _test_can_load_parameters_within_python(self, script_directory, expected_loaded_parameters, check_for_warning=False):
        self._test_command_that_loads_parameters_in_directory_for_python(['python', 'main.py'], script_directory, expected_loaded_parameters, check_for_warning)

    def _test_can_load_parameters_within_foundations_submit(self, script_directory, expected_loaded_parameters):
        self._test_command_that_loads_parameters_in_directory(['python', '-m', 'foundations', 'submit','--project-name', self.project_name, '--entrypoint', 'project_code/script_to_run.py'], script_directory, expected_loaded_parameters)

    def _test_command_that_loads_parameters_in_directory(self, command, script_directory, expected_loaded_parameters):
        from foundations_internal.change_directory import ChangeDirectory

        import subprocess
        import json
        import os
        import os.path as path

        env = self._update_environment_with_home_directory()

        with ChangeDirectory(script_directory):
            completed_process = subprocess.run(command, stdout=subprocess.PIPE, env=env)
            process_output = completed_process.stdout.decode().strip().split('\n')

        params_json = process_output[-1]
        job_id = process_output[-2]
        project_name = self.project_name

        result_parameters = json.loads(params_json)
        self.assertEqual(expected_loaded_parameters, result_parameters)
        self._assert_flattened_parameter_keys_in_project_job_parameter_names_set(project_name, expected_loaded_parameters)
        self._assert_flattened_parameter_values_for_job_in_job_parameters(job_id, expected_loaded_parameters)
        self._assert_flattened_parameter_keys_in_project_input_parameter_names_set(project_name, expected_loaded_parameters)
        self._assert_flattened_parameter_names_for_job_in_job_input_parameters(job_id, expected_loaded_parameters)

    def _test_command_that_loads_parameters_in_directory_for_python(self, command, script_directory, expected_loaded_parameters, check_for_warning):
        from foundations_internal.change_directory import ChangeDirectory

        import subprocess
        import json
        import os.path as path

        env = self._update_environment_with_home_directory()

        with ChangeDirectory(script_directory):
            env = None if check_for_warning else env
            completed_process = subprocess.run(command, stdout=subprocess.PIPE, env=env)
            process_output = completed_process.stdout.decode()

        warnings, _, params_json = process_output.strip().rpartition('\n')
        if check_for_warning:
            self.assertIn('Script not run with Foundations.', warnings)

        result_parameters = json.loads(params_json)
        self.assertEqual(expected_loaded_parameters, result_parameters)

    def _assert_flattened_parameter_keys_in_project_job_parameter_names_set(self, project_name, expected_loaded_parameters):
        from foundations.job_parameters import flatten_parameter_dictionary
        from foundations_contrib.global_state import redis_connection

        flattened_parameters = flatten_parameter_dictionary(expected_loaded_parameters)
        parameter_names = set(map(lambda param_name: bytes(param_name, 'ascii'), flattened_parameters))
        logged_parameter_names = redis_connection.smembers('projects:{}:job_parameter_names'.format(project_name))
        self.assertEqual(parameter_names, logged_parameter_names)

    def _assert_flattened_parameter_values_for_job_in_job_parameters(self, job_id, expected_loaded_parameters):
        from foundations.job_parameters import flatten_parameter_dictionary
        from foundations_contrib.global_state import redis_connection

        import json

        flattened_parameters = flatten_parameter_dictionary(expected_loaded_parameters)

        parameters_in_redis = redis_connection.get('jobs:{}:parameters'.format(job_id))

        if parameters_in_redis is None:
            logged_parameters = {}
        else:
            logged_parameters = json.loads(parameters_in_redis)

        self.assertEqual(flattened_parameters, logged_parameters)

    def _assert_flattened_parameter_keys_in_project_input_parameter_names_set(self, project_name, expected_loaded_parameters):
        from foundations.job_parameters import flatten_parameter_dictionary
        from foundations_contrib.global_state import redis_connection

        flattened_parameters = flatten_parameter_dictionary(expected_loaded_parameters)
        parameter_names = set(map(lambda param_key: bytes(param_key, 'ascii'),flattened_parameters))
        logged_parameter_names = redis_connection.smembers('projects:{}:input_parameter_names'.format(project_name))
        self.assertEqual(parameter_names, logged_parameter_names)

    def _assert_flattened_parameter_names_for_job_in_job_input_parameters(self, job_id, expected_loaded_parameters):
        from foundations.job_parameters import flatten_parameter_dictionary
        from foundations_contrib.global_state import redis_connection
        from foundations_internal.foundations_serializer import loads

        flattened_parameters = flatten_parameter_dictionary(expected_loaded_parameters)

        flattened_parameters_data = []

        for parameter_name in flattened_parameters.keys():
            flattened_parameters_data.append({'argument': {'name': parameter_name, 'value': {'type': 'dynamic', 'name': parameter_name}}, 'stage_uuid': 'stageless'})

        logged_parameters = redis_connection.get('jobs:{}:input_parameters'.format(job_id))
        self.assertEqual(flattened_parameters_data, loads(logged_parameters))