
import unittest
from mock import Mock

from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers import let, let_mock, set_up

class TestDeploymentContextBucket(Spec):

    @let
    def config_manager(self):
        from foundations_contrib.config_manager import ConfigManager

        config_manager = ConfigManager()
        return self.patch('foundations_contrib.global_state.config_manager', config_manager)

    @set_up
    def set_up(self):
        # ensure we use our config manager
        self.config_manager

    @let
    def context_bucket(self):
        from foundations_contrib.deployment_context_bucket import DeploymentContextBucket
        return DeploymentContextBucket(self.local_bucket, self.deploy_bucket)

    local_bucket = let_mock()    
    deploy_bucket = let_mock()
    name = let_mock()
    data = let_mock()
    input_file = let_mock()
    output_file = let_mock()
    dummy = let_mock()
    pathname = let_mock()
    source = let_mock()
    destination = let_mock()

    def test_upload_from_string_calls_local(self):
        self.local_bucket.upload_from_string.return_value = self.dummy
        result = self.context_bucket.upload_from_string(self.name, self.data)
        self.local_bucket.upload_from_string.assert_called_with(self.name, self.data)
        self.assertEqual(self.dummy, result)

    def test_upload_from_string_calls_deploy_when_in_deplyment(self):
        self.config_manager['_is_deployment'] = True

        self.deploy_bucket.upload_from_string.return_value = self.dummy
        result = self.context_bucket.upload_from_string(self.name, self.data)
        self.deploy_bucket.upload_from_string.assert_called_with(self.name, self.data)
        self.assertEqual(self.dummy, result)

    def test_upload_from_file_calls_local(self):
        self.local_bucket.upload_from_file.return_value = self.dummy
        result = self.context_bucket.upload_from_file(self.name, self.input_file)
        self.local_bucket.upload_from_file.assert_called_with(self.name, self.input_file)
        self.assertEqual(self.dummy, result)

    def test_upload_from_file_calls_deploy_when_in_deplyment(self):
        self.config_manager['_is_deployment'] = True

        self.deploy_bucket.upload_from_file.return_value = self.dummy
        result = self.context_bucket.upload_from_file(self.name, self.input_file)
        self.deploy_bucket.upload_from_file.assert_called_with(self.name, self.input_file)
        self.assertEqual(self.dummy, result)

    def test_exists_calls_local(self):
        self.local_bucket.exists.return_value = self.dummy
        result = self.context_bucket.exists(self.name)
        self.local_bucket.exists.assert_called_with(self.name)
        self.assertEqual(self.dummy, result)

    def test_exists_calls_deploy_when_in_deplyment(self):
        self.config_manager['_is_deployment'] = True

        self.deploy_bucket.exists.return_value = self.dummy
        result = self.context_bucket.exists(self.name)
        self.deploy_bucket.exists.assert_called_with(self.name)
        self.assertEqual(self.dummy, result)

    def test_download_as_string_calls_local(self):
        self.local_bucket.download_as_string.return_value = self.dummy
        result = self.context_bucket.download_as_string(self.name)
        self.local_bucket.download_as_string.assert_called_with(self.name)
        self.assertEqual(self.dummy, result)

    def test_download_as_string_calls_deploy_when_in_deplyment(self):
        self.config_manager['_is_deployment'] = True

        self.deploy_bucket.download_as_string.return_value = self.dummy
        result = self.context_bucket.download_as_string(self.name)
        self.deploy_bucket.download_as_string.assert_called_with(self.name)
        self.assertEqual(self.dummy, result)

    def test_download_to_file_calls_local(self):
        self.local_bucket.download_to_file.return_value = self.dummy
        result = self.context_bucket.download_to_file(self.name, self.output_file)
        self.local_bucket.download_to_file.assert_called_with(self.name, self.output_file)
        self.assertEqual(self.dummy, result)

    def test_download_to_file_calls_deploy_when_in_deplyment(self):
        self.config_manager['_is_deployment'] = True

        self.deploy_bucket.download_to_file.return_value = self.dummy
        result = self.context_bucket.download_to_file(self.name, self.output_file)
        self.deploy_bucket.download_to_file.assert_called_with(self.name, self.output_file)
        self.assertEqual(self.dummy, result)

    def test_list_files_calls_local(self):
        self.local_bucket.list_files.return_value = self.dummy
        result = self.context_bucket.list_files(self.pathname)
        self.local_bucket.list_files.assert_called_with(self.pathname)
        self.assertEqual(self.dummy, result)

    def test_list_files_calls_deploy_when_in_deplyment(self):
        self.config_manager['_is_deployment'] = True

        self.deploy_bucket.list_files.return_value = self.dummy
        result = self.context_bucket.list_files(self.pathname)
        self.deploy_bucket.list_files.assert_called_with(self.pathname)
        self.assertEqual(self.dummy, result)

    def test_remove_calls_local(self):
        self.local_bucket.remove.return_value = self.dummy
        result = self.context_bucket.remove(self.name)
        self.local_bucket.remove.assert_called_with(self.name)
        self.assertEqual(self.dummy, result)

    def test_remove_calls_deploy_when_in_deplyment(self):
        self.config_manager['_is_deployment'] = True

        self.deploy_bucket.remove.return_value = self.dummy
        result = self.context_bucket.remove(self.name)
        self.deploy_bucket.remove.assert_called_with(self.name)
        self.assertEqual(self.dummy, result)

    def test_move_calls_local(self):
        self.local_bucket.move.return_value = self.dummy
        result = self.context_bucket.move(self.source, self.destination)
        self.local_bucket.move.assert_called_with(self.source, self.destination)
        self.assertEqual(self.dummy, result)

    def test_move_calls_deploy_when_in_deplyment(self):
        self.config_manager['_is_deployment'] = True

        self.deploy_bucket.move.return_value = self.dummy
        result = self.context_bucket.move(self.source, self.destination)
        self.deploy_bucket.move.assert_called_with(self.source, self.destination)
        self.assertEqual(self.dummy, result)
