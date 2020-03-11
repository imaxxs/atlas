
import unittest
from mock import Mock

from foundations_spec.helpers.spec import Spec
from foundations_spec.helpers.conditional_return import ConditionalReturn
from foundations_spec.helpers import set_up, let, let_mock, let_now, let_patch_mock

class TestConnectionManager(Spec):

    mock_authorization_instance = let_mock()
    mock_connection_instance = let_mock()

    @let
    def connection_manager(self):
        from foundations_gcp.connection_manager import ConnectionManager
        return ConnectionManager()

    @set_up
    def set_up(self):
        self.mock_authorization = self.patch('foundations_gcp.authorized_storage_session.AuthorizedStorageSession', ConditionalReturn())
        self.mock_authorization.return_when(
            self.mock_authorization_instance, 
            pool_size=30,
            pool_block=True,
            max_retries=3
        )
        self.mock_connection = self.patch('google.cloud.storage.Client', ConditionalReturn())
        self.mock_connection.return_when(self.mock_connection_instance, _http=self.mock_authorization_instance)
    
    def test_bucket_connection_creates_connection(self):
        self.assertEqual(self.connection_manager.bucket_connection(), self.mock_connection_instance)
    
    def test_bucket_connection_reuses_connection(self):
        self.connection_manager.bucket_connection()
        self.connection_manager.bucket_connection()
        self.mock_connection.assert_called_once()