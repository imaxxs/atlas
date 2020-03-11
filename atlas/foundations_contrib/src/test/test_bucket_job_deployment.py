
import unittest

from mock import patch, Mock, mock_open

from foundations_contrib.bucket_job_deployment import BucketJobDeployment

from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers import let

class TestBucketJobDeployment(Spec):
    
    _mock_open = mock_open()

    @let
    def deployment(self):
        return BucketJobDeployment(self.job_name, self.job, self.job_source_bundle, self.code_bucket, self.result_bucket)

    @let
    def job_name(self):
        return self.faker.name()

    @let
    def job(self):
        return Mock()

    @let
    def job_source_bundle(self):
        return Mock()

    @let
    def code_bucket(self):
        return Mock()

    @let
    def result_bucket(self):
        return Mock()

    def test_config_includes_deploy_flag(self):
        self.assertTrue(self.deployment.config()['_is_deployment'])

    @patch('foundations_contrib.bucket_job_deployment.BucketJobDeployment._bucket_upload_from_file', Mock())
    def test_upload_to_result_bucket_calls_bucket_upload_from_file_with_result_bucket(self):
        self.deployment.upload_to_result_bucket()
        self.deployment._bucket_upload_from_file.assert_called_with(self.result_bucket)


    @patch('builtins.open', _mock_open)
    def test_upload_to_result_bucket_opens_job_archive(self):
        self.deployment.upload_to_result_bucket()
        open.assert_called_with(self.deployment._job_archive(), 'rb')

    @patch('builtins.open', _mock_open, create=True)
    def test_upload_to_result_bucket_calls_upload_from_file_from_result_bucket_with_job_archive_name_and_file(self):
        self.deployment.upload_to_result_bucket()
        self.deployment._result_bucket.upload_from_file.assert_called_with(self.deployment._job_archive_name(), self._mock_open())
